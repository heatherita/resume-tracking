from schemas.schemas import UserBase
from models.models import Role, Job, Application, Artifact, ArtifactMetric, Section, User, artifact_sections

from sqlalchemy.orm import Session
from sqlalchemy import select, func


def get_target_order(artifact_id:int, db:Session) -> int:
    
    max_order = db.execute(
        select(func.max(artifact_sections.c.section_order)).where(artifact_sections.c.artifact_id == artifact_id)
    ).scalar_one_or_none()
    next_order = (max_order or 0) + 1
    target_order = next_order
    return target_order

def get_user_by_username(username:str, db:Session):
    user_orm = db.query(User).filter(User.username == username).first()
    return UserBase.from_orm(user_orm) if user_orm else None

# def insert_user(name:str, email:str, address:str, db:Session):
#     new_user = User(name=name)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user