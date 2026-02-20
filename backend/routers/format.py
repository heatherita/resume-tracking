
from pathlib import Path
from typing import Any
import logging
from schemas.document_schemas import CoverLetterRequest
from schemas.schemas import ArtifactTypeEnum
from models.models import Application
from services.document_service import build_cover_letter, create_cover_letter_odt_from_md, create_pdf_from_md
from database import get_db
import config
from config.settings import BASE_STORAGE_PATH
from services.resume_service import build_md, create_odt_from_md, create_resume_pdf_from_md, create_resume_pdf_from_md, load_yaml
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
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
    return FileResponse(path=resume_path, filename=resume_path.name, media_type="text/markdown")

@router.post("/resume/create/odt")
def create_odt_resume():
    odt_path = create_odt_from_md()
    return FileResponse(path=odt_path, filename=odt_path.name, media_type="application/vnd.oasis.opendocument.text")


@router.post("/resume/create/pdf")
def create_pdf_resume(pdf_engine: str = "tectonic"):
    pdf_path = create_pdf_from_md(ArtifactTypeEnum.resume, pdf_engine=pdf_engine)
    return FileResponse(path=pdf_path, filename=pdf_path.name, media_type="application/pdf")

@router.post("/cover-letter/create/md")
def create_markdown_cover_letter(c:CoverLetterRequest, db: Session = Depends(get_db)):
    logger.info(f"Received request to create markdown cover letter for application id {c.application_id}")
    md = build_cover_letter(c.username, c.application_id, db)
    artifact_name = ArtifactTypeEnum.cover_letter.value
    cover_letter_path = Path(BASE_STORAGE_PATH) / f"{artifact_name}_{c.application_id}.md"
    cover_letter_path.write_text(md, encoding="utf-8")
    return FileResponse(path=cover_letter_path, filename=cover_letter_path.name, media_type="text/markdown") 

@router.post("/cover_letter/create/odt")
def create_odt_cover_letter(c:CoverLetterRequest, db: Session = Depends(get_db)):
    odt_path = create_cover_letter_odt_from_md(ArtifactTypeEnum.cover_letter, c.application_id)
    return FileResponse(path=odt_path, filename=odt_path.name, media_type="application/vnd.oasis.opendocument.text")
    
@router.post("/cover-letter/create/pdf")
def create_pdf_cover_letter(c:CoverLetterRequest, db: Session = Depends(get_db)):
    logger.info(f"Received request to create PDF cover letter for application id {c.application_id}")
    pdf_path = create_pdf_from_md(ArtifactTypeEnum.cover_letter, c.application_id, pdf_engine="tectonic")
    return FileResponse(path=pdf_path, filename=pdf_path.name, media_type="application/pdf") 
