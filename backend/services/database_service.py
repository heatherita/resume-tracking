from models.models import Role, Job, Application, Artifact, ArtifactMetric, Section, artifact_sections

from sqlalchemy.orm import Session
from sqlalchemy import select, func


def get_target_order(artifact_id:int, db:Session) -> int:
    
    
    max_order = db.execute(
        select(func.max(artifact_sections.c.section_order)).where(artifact_sections.c.artifact_id == artifact_id)
    ).scalar_one_or_none()
    next_order = (max_order or 0) + 1
    target_order = next_order
    return target_order