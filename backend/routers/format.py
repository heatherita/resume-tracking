
from pathlib import Path
from typing import Any
import logging
from schemas.document_schemas import CoverLetterRequest
from schemas.schemas import ArtifactTypeEnum
from models.models import Application
from services.document_service import build_cover_letter, create_pdf_from_md
from database import get_db
import config
from config.settings import BASE_STORAGE_PATH
from services.resume_service import build_md, create_odt_from_md, create_resume_pdf_from_md, create_resume_pdf_from_md, load_yaml
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger("jobtelem")


@router.post("/resume/create/md")
def create_markdown_resume(resume_data: dict[str, Any]):
    # include = resume_data.get("include").split(",") if resume_data.get("include") else []
    # exclude = set(resume_data.get("exclude", []))
    include = {t.strip().lower() for t in resume_data.get("include").split(",") if t.strip()}
    exclude = {t.strip().lower() for t in resume_data.get("exclude").split(",") if t.strip()}

    mode = resume_data.get("mode", "any")

    data = load_yaml(Path("config/resume.yaml"))
    md = build_md(data, include, exclude, mode)
    resume_path = Path(BASE_STORAGE_PATH) / "resume.md"
    resume_path.write_text(md, encoding="utf-8")

@router.post("/resume/create/odt")
def create_odt_resume():
    create_odt_from_md()


@router.post("/resume/create/pdf")
def create_pdf_resume(pdf_engine: str = "tectonic"):
    create_pdf_from_md(ArtifactTypeEnum.resume, pdf_engine=pdf_engine)
    
@router.post("/cover-letter/create/md")
def create_markdown_cover_letter(c:CoverLetterRequest, db: Session = Depends(get_db)):
    logger.info(f"Received request to create markdown cover letter for application id {c.application_id}")
    md = build_cover_letter(c.username, c.application_id, db)
    artifact_name = ArtifactTypeEnum.cover_letter.value
    cover_letter_path = Path(BASE_STORAGE_PATH) / f"{artifact_name}_{c.application_id}.md"
    cover_letter_path.write_text(md, encoding="utf-8")
    
@router.get("/cover-letter/create/pdf")
def create_pdf_cover_letter(application_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to create PDF cover letter for application id {application_id}")
    create_pdf_from_md(ArtifactTypeEnum.cover_letter, application_id, pdf_engine="tectonic")
    
