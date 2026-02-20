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

def build_cover_letter(username:str, application_id:int, db:Session) -> str:
    letter_parts = []
    user = get_user_by_username(username, db)
    if not user:
        raise ValueError(f"User with username {username} not found")
    application = db.query(Application).filter(Application.id == application_id).first()
    logger.info(f"Building cover letter for application id {application_id} with  name {Application.contact if Application else 'N/A'}")
    if not Application:
        raise ValueError(f"Application with id {application_id} not found")
    
    job = db.query(Job).filter(Job.id == Application.job_id).first()
    if not job:
        raise ValueError(f"Job with id {Application.job_id} not found")
    artifacts = db.query(Artifact).filter(and_(Artifact.application_id == application_id, Artifact.type == ArtifactTypeEnum.cover_letter)).first()
    if not artifacts:
        raise ValueError(f"Cover letter artifact for application id {application_id} not found")
    sections = db.query(Section).join(artifact_sections).filter(artifact_sections.c.artifact_id == artifacts.id).order_by(artifact_sections.c.section_order).all()
    if not sections:
        raise ValueError(f"No sections found for cover letter artifact id {artifacts.id}")
    
    letter_parts.append(f"{user.full_name}")  
    letter_parts.append(f"{user.email}")
    address = user.address if user.address else "N/A"
    letter_parts.append(f"{address}")  
    
    date_str = datetime.now().strftime("%B %d, %Y")
    letter_parts.append(date_str)
    letter_parts.append("")  # Blank line
    
    contact_name = application.contact if application.contact else "Hiring Manager"
    letter_parts.append(f"Dear {contact_name},")
    for section in sections:
        letter_parts.append(section.content)
    return "\n\n".join(letter_parts)

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