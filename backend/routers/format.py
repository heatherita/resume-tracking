
from pathlib import Path
from typing import Any
import config
from config.settings import BASE_STORAGE_PATH
from services.resume_service import build_md, load_yaml
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/resume/create/md")
def create_markdown_resume(resume_data: dict[str, Any]):
    include = set(resume_data.get("include", []))
    exclude = set(resume_data.get("exclude", []))
    mode = resume_data.get("mode", "any")

    data = load_yaml(Path("config/resume.yaml"))
    md = build_md(data, include, exclude, mode)
    resume_path = Path(BASE_STORAGE_PATH) / "resume.md"
    resume_path.write_text(md, encoding="utf-8")


