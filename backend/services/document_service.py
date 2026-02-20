from __future__ import annotations

import argparse
from datetime import datetime
import shutil
import subprocess
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import psycopg2
import yaml
from services.database_service import get_user_by_username
from schemas.schemas import ArtifactTypeEnum
from config.settings import BASE_STORAGE_PATH
from models.models import Role, Job, Application, Artifact, ArtifactMetric, Section, artifact_sections

from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_

logger = logging.getLogger("jobtelem")

def build_cover_letter(username: str, application_id: int, db: Session) -> str:
    user = get_user_by_username(username, db)
    if not user:
        raise ValueError(f"User with username {username} not found")

    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise ValueError(f"Application with id {application_id} not found")

    job = db.query(Job).filter(Job.id == application.job_id).first()
    if not job:
        raise ValueError(f"Job with id {application.job_id} not found")

    artifact = (
        db.query(Artifact)
        .filter(and_(
            Artifact.application_id == application_id,
            Artifact.type == ArtifactTypeEnum.cover_letter
        ))
        .first()
    )
    if not artifact:
        raise ValueError(f"Cover letter artifact for application id {application_id} not found")

    sections = (
        db.query(Section)
        .join(artifact_sections)
        .filter(artifact_sections.c.artifact_id == artifact.id)
        .order_by(artifact_sections.c.section_order)
        .all()
    )
    if not sections:
        raise ValueError(f"No sections found for cover letter artifact id {artifact.id}")

    contact = application.contact or "Hiring Manager"
    date_str = datetime.now().strftime("%B %d, %Y")

    # Address/date block (single newlines inside block)
    header_lines = [
        f"{user.full_name}  ",
        f"{user.address}  ",
        f"{user.city}, {user.state} {user.postal_code}  ",
    ]
    if user.phone:
        header_lines.append(user.phone)
    header_block = "\n".join(line for line in header_lines if line)

    recipient_lines = [
        f"{contact}  ",
        f"{job.company or ''}  ",
        f"{application.contact_address or ''}  ",
    ]
    recipient_block = "\n".join(line for line in recipient_lines if line)

    # Body paragraphs (double newlines between paragraphs)
    body_paragraphs = [section.content.strip() for section in sections if section.content and section.content.strip()]

    if job.required_skills:
        body_paragraphs.append(
            f"In particular, I believe my experience with {job.required_skills} would allow me to make an immediate contribution to your team."
        )
    if job.title and job.company:
        body_paragraphs.append(
            f"I am confident that my years of experience make me a strong candidate for the {job.title} role at {job.company}."
        )

    closing_block = "\n".join([
        "Sincerely,  ",
        f"{user.full_name}  ",
        f"{user.email}  ",
    ])

    blocks = [
        header_block,
        date_str,
        recipient_block,
        f"Dear {contact},",
        "\n\n".join(body_paragraphs),
        closing_block,
    ]

    # Critical: blank line between major blocks for markdown->latex paragraph spacing
    return "\n\n  ".join(block for block in blocks if block.strip())

def create_cover_letter_odt_from_md(artifact_type:ArtifactTypeEnum, application_id:int = None):
    artifact_name = artifact_type.value
    if artifact_type == ArtifactTypeEnum.cover_letter:
        # template_name = "cover_letter_template.tex"
        file_base_name = f"{artifact_name}_{application_id}"
    else:
        # template_name = "resume_template.tex"
        file_base_name = f"{artifact_name}"
    md_path = Path(BASE_STORAGE_PATH) / f"{file_base_name}.md"
    odt_path = Path(BASE_STORAGE_PATH) / f"{file_base_name}.odt"
    # template_path = Path(__file__).resolve().parents[1] / "config" / template_name
    
    ref_doc_path = Path(__file__).resolve().parents[1] / "config" / "custom-reference.odt"
    cmd = [
    "pandoc",
    str(md_path),
    "--reference-doc", str(ref_doc_path),
    "-t","odt",
    "-o", str(odt_path),
    ]    
    subprocess.run(cmd, check=True)
    return odt_path

def create_pdf_from_md(artifact_type:ArtifactTypeEnum, application_id:int = None, pdf_engine: str = "tectonic"):
    artifact_name = artifact_type.value
    if artifact_type == ArtifactTypeEnum.cover_letter:
        template_name = "cover_letter_template.tex"
        file_base_name = f"{artifact_name}_{application_id}"
    else:
        template_name = "resume_template.tex"
        file_base_name = f"{artifact_name}"
    md_path = Path(BASE_STORAGE_PATH) / f"{file_base_name}.md"
    pdf_path = Path(BASE_STORAGE_PATH) / f"{file_base_name}.pdf"
    template_path = Path(__file__).resolve().parents[1] / "config" / template_name
    cmd = [
        "pandoc",
        str(md_path),
        "--pdf-engine", "xelatex",
        "--template", str(template_path),
        # "-V", "geometry:margin=0.75in",
        "-V", "fontsize=10pt",
        "-V", "mainfont=DejaVu Sans",
        "-V", "sansfont=DejaVu Sans",
        # "-V", "linestretch=1.05",
        "-o", str(pdf_path),
    ]
    subprocess.run(cmd, check=True)
    return pdf_path