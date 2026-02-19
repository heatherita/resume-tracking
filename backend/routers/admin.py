from typing import List
from database import get_db
from models.models import Role, Job, Application, Artifact, ArtifactMetric, Section
from schemas.schemas import (
    ArtifactMetricOut,
    RoleOut,
    JobOut,
    ApplicationOut,
    ArtifactOut,
    ApplicationCreate,
    ApplicationUpdate,
    ArtifactCreate,
    ArtifactMetricCreate,
    ArtifactMetricUpdate,
    ArtifactUpdate,
    JobCreate,
    JobUpdate,
    RoleCreate,
    RoleUpdate,
    SectionCreate,
    SectionUpdate,
    SectionOut,
)
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

logger = logging.getLogger("jobtelem")
router = APIRouter()


@router.post("/roles/", response_model=RoleOut, tags=["roles"])
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.get("/roles/", response_model=List[RoleOut], tags=["roles"])
async def get_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@router.get("/roles/{role_id}", response_model=RoleOut, tags=["roles"])
async def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/roles/{role_id}", response_model=RoleOut, tags=["roles"])
async def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    update_data = role.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_role, key, value)
    
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.delete("/roles/{role_id}", tags=["roles"])
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}


# ===================== JOBS =====================

@router.post("/jobs/", response_model=JobOut, tags=["jobs"])
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    # Verify role exists
    role = db.query(Role).filter(Role.id == job.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/jobs/", response_model=List[JobOut], tags=["jobs"])
async def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs


@router.get("/jobs/{job_id}", response_model=JobOut, tags=["jobs"])
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
   
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/jobs/{job_id}", response_model=JobOut, tags=["jobs"])
async def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = job.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job, key, value)
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.delete("/jobs/{job_id}", tags=["jobs"])
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}


# ===================== ARTIFACTS =====================

@router.post("/artifacts/", response_model=ArtifactOut, tags=["artifacts"])
async def create_artifact(artifact: ArtifactCreate, db: Session = Depends(get_db)):
    db_artifact = Artifact(**artifact.dict())
    db.add(db_artifact)
    db.commit()
    db.refresh(db_artifact)
    return db_artifact


@router.get("/artifacts/", response_model=List[ArtifactOut], tags=["artifacts"])
async def get_artifacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    artifacts = db.query(Artifact).offset(skip).limit(limit).all()
    return artifacts


@router.get("/artifacts/{artifact_id}", response_model=ArtifactOut, tags=["artifacts"])
async def get_artifact(artifact_id: int, db: Session = Depends(get_db)):
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact


@router.put("/artifacts/{artifact_id}", response_model=ArtifactOut, tags=["artifacts"])
async def update_artifact(artifact_id: int, artifact: ArtifactUpdate, db: Session = Depends(get_db)):
    db_artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not db_artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    
    update_data = artifact.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_artifact, key, value)
    
    db.add(db_artifact)
    db.commit()
    db.refresh(db_artifact)
    return db_artifact


@router.delete("/artifacts/{artifact_id}", tags=["artifacts"])
async def delete_artifact(artifact_id: int, db: Session = Depends(get_db)):
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    db.delete(artifact)
    db.commit()
    return {"message": "Artifact deleted successfully"}


# ===================== SECTIONS =====================

@router.post("/sections/", response_model=SectionOut, tags=["sections"])
async def create_section(section: SectionCreate, db: Session = Depends(get_db)):
    db_section = Section(**section.dict())
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section


@router.get("/sections/", response_model=List[SectionOut], tags=["sections"])
async def get_sections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sections = db.query(Section).order_by(Section.order.asc(), Section.id.asc()).offset(skip).limit(limit).all()
    return sections


@router.get("/sections/{section_id}", response_model=SectionOut, tags=["sections"])
async def get_section(section_id: int, db: Session = Depends(get_db)):
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.put("/sections/{section_id}", response_model=SectionOut, tags=["sections"])
async def update_section(section_id: int, section: SectionUpdate, db: Session = Depends(get_db)):
    db_section = db.query(Section).filter(Section.id == section_id).first()
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")

    update_data = section.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_section, key, value)

    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section


@router.delete("/sections/{section_id}", tags=["sections"])
async def delete_section(section_id: int, db: Session = Depends(get_db)):
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    db.delete(section)
    db.commit()
    return {"message": "Section deleted successfully"}


@router.get("/artifacts/{artifact_id}/sections/", response_model=List[SectionOut], tags=["sections"])
async def get_artifact_sections(artifact_id: int, db: Session = Depends(get_db)):
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact.sections


@router.post("/artifacts/{artifact_id}/sections/", response_model=SectionOut, tags=["sections"])
async def create_section_for_artifact(artifact_id: int, section: SectionCreate, db: Session = Depends(get_db)):
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    db_section = Section(**section.dict())
    artifact.sections.append(db_section)
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section


@router.post("/artifacts/{artifact_id}/sections/{section_id}", tags=["sections"])
async def attach_section_to_artifact(artifact_id: int, section_id: int, db: Session = Depends(get_db)):
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    if section not in artifact.sections:
        artifact.sections.append(section)
        db.commit()

    return {"message": "Section attached to artifact"}


@router.delete("/artifacts/{artifact_id}/sections/{section_id}", tags=["sections"])
async def detach_section_from_artifact(artifact_id: int, section_id: int, db: Session = Depends(get_db)):
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    if section in artifact.sections:
        artifact.sections.remove(section)
        db.commit()

    return {"message": "Section detached from artifact"}


# ===================== ARTIFACT METRICS =====================

@router.post("/artifacts/{artifact_id}/metrics/", response_model=ArtifactMetricOut, tags=["artifact_metrics"])
async def create_artifact_metric(artifact_id: int, metric: ArtifactMetricCreate, db: Session = Depends(get_db)):
    # Verify artifact exists
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    
    db_metric = ArtifactMetric(artifact_id=artifact_id, **metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.get("/artifacts/{artifact_id}/metrics/", response_model=List[ArtifactMetricOut], tags=["artifact_metrics"])
async def get_artifact_metrics(artifact_id: int, db: Session = Depends(get_db)):
    metrics = db.query(ArtifactMetric).filter(ArtifactMetric.artifact_id == artifact_id).all()
    return metrics


@router.put("/metrics/{metric_id}", response_model=ArtifactMetricOut, tags=["artifact_metrics"])
async def update_artifact_metric(metric_id: int, metric: ArtifactMetricUpdate, db: Session = Depends(get_db)):
    db_metric = db.query(ArtifactMetric).filter(ArtifactMetric.id == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    update_data = metric.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_metric, key, value)
    
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.delete("/metrics/{metric_id}", tags=["artifact_metrics"])
async def delete_artifact_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(ArtifactMetric).filter(ArtifactMetric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    db.delete(metric)
    db.commit()
    return {"message": "Metric deleted successfully"}


# ===================== APPLICATIONS =====================

@router.post("/applications/", response_model=ApplicationOut, tags=["applications"])
async def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    # Verify job exists
    job = db.query(Job).filter(Job.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_application = Application(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


@router.get("/applications/", response_model=List[ApplicationOut], tags=["applications"])
async def get_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applications = db.query(Application).offset(skip).limit(limit).all()
    return applications


@router.get("/applications/{application_id}", response_model=ApplicationOut, tags=["applications"])
async def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.put("/applications/{application_id}", response_model=ApplicationOut, tags=["applications"])
async def update_application(application_id: int, application: ApplicationUpdate, db: Session = Depends(get_db)):
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    update_data = application.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_application, key, value)
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


@router.delete("/applications/{application_id}", tags=["applications"])
async def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return {"message": "Application deleted successfully"}
