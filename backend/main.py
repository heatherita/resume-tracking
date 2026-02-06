from config.settings import APP_NAME
from config.logging_config import setup_logger
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, get_db
from models.models import Role as RoleModel, Job as JobModel, Application as ApplicationModel, Artifact as ArtifactModel, ArtifactMetric as ArtifactMetricModel
from schemas.schemas import (
    Role, RoleCreate, RoleUpdate,
    Job, JobCreate, JobUpdate, JobWithApplications,
    Application, ApplicationCreate, ApplicationUpdate, ApplicationWithArtifacts,
    Artifact, ArtifactCreate, ArtifactUpdate, ArtifactWithMetrics,
    ArtifactMetric, ArtifactMetricCreate, ArtifactMetricUpdate
)
# from config import get_settings


logger = setup_logger()
logger.info("Backend started")


# settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================== ROLES =====================

@app.post("/api/roles/", response_model=Role, tags=["roles"])
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = RoleModel(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@app.get("/api/roles/", response_model=List[Role], tags=["roles"])
async def get_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = db.query(RoleModel).offset(skip).limit(limit).all()
    return roles


@app.get("/api/roles/{role_id}", response_model=Role, tags=["roles"])
async def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@app.put("/api/roles/{role_id}", response_model=Role, tags=["roles"])
async def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    update_data = role.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_role, key, value)
    
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@app.delete("/api/roles/{role_id}", tags=["roles"])
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}


# ===================== JOBS =====================

@app.post("/api/jobs/", response_model=Job, tags=["jobs"])
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    # Verify role exists
    role = db.query(RoleModel).filter(RoleModel.id == job.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db_job = JobModel(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@app.get("/api/jobs/", response_model=List[Job], tags=["jobs"])
async def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(JobModel).offset(skip).limit(limit).all()
    return jobs


@app.get("/api/jobs/{job_id}", response_model=JobWithApplications, tags=["jobs"])
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.put("/api/jobs/{job_id}", response_model=Job, tags=["jobs"])
async def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = job.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job, key, value)
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@app.delete("/api/jobs/{job_id}", tags=["jobs"])
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}


# ===================== ARTIFACTS =====================

@app.post("/api/artifacts/", response_model=Artifact, tags=["artifacts"])
async def create_artifact(artifact: ArtifactCreate, db: Session = Depends(get_db)):
    db_artifact = ArtifactModel(**artifact.dict())
    db.add(db_artifact)
    db.commit()
    db.refresh(db_artifact)
    return db_artifact


@app.get("/api/artifacts/", response_model=List[Artifact], tags=["artifacts"])
async def get_artifacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    artifacts = db.query(ArtifactModel).offset(skip).limit(limit).all()
    return artifacts


@app.get("/api/artifacts/{artifact_id}", response_model=ArtifactWithMetrics, tags=["artifacts"])
async def get_artifact(artifact_id: int, db: Session = Depends(get_db)):
    artifact = db.query(ArtifactModel).filter(ArtifactModel.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact


@app.put("/api/artifacts/{artifact_id}", response_model=Artifact, tags=["artifacts"])
async def update_artifact(artifact_id: int, artifact: ArtifactUpdate, db: Session = Depends(get_db)):
    db_artifact = db.query(ArtifactModel).filter(ArtifactModel.id == artifact_id).first()
    if not db_artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    
    update_data = artifact.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_artifact, key, value)
    
    db.add(db_artifact)
    db.commit()
    db.refresh(db_artifact)
    return db_artifact


@app.delete("/api/artifacts/{artifact_id}", tags=["artifacts"])
async def delete_artifact(artifact_id: int, db: Session = Depends(get_db)):
    artifact = db.query(ArtifactModel).filter(ArtifactModel.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    db.delete(artifact)
    db.commit()
    return {"message": "Artifact deleted successfully"}


# ===================== ARTIFACT METRICS =====================

@app.post("/api/artifacts/{artifact_id}/metrics/", response_model=ArtifactMetric, tags=["artifact_metrics"])
async def create_artifact_metric(artifact_id: int, metric: ArtifactMetricCreate, db: Session = Depends(get_db)):
    # Verify artifact exists
    artifact = db.query(ArtifactModel).filter(ArtifactModel.id == artifact_id).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    
    db_metric = ArtifactMetricModel(artifact_id=artifact_id, **metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@app.get("/api/artifacts/{artifact_id}/metrics/", response_model=List[ArtifactMetric], tags=["artifact_metrics"])
async def get_artifact_metrics(artifact_id: int, db: Session = Depends(get_db)):
    metrics = db.query(ArtifactMetricModel).filter(ArtifactMetricModel.artifact_id == artifact_id).all()
    return metrics


@app.put("/api/metrics/{metric_id}", response_model=ArtifactMetric, tags=["artifact_metrics"])
async def update_artifact_metric(metric_id: int, metric: ArtifactMetricUpdate, db: Session = Depends(get_db)):
    db_metric = db.query(ArtifactMetricModel).filter(ArtifactMetricModel.id == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    update_data = metric.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_metric, key, value)
    
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@app.delete("/api/metrics/{metric_id}", tags=["artifact_metrics"])
async def delete_artifact_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(ArtifactMetricModel).filter(ArtifactMetricModel.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    db.delete(metric)
    db.commit()
    return {"message": "Metric deleted successfully"}


# ===================== APPLICATIONS =====================

@app.post("/api/applications/", response_model=Application, tags=["applications"])
async def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    # Verify job exists
    job = db.query(JobModel).filter(JobModel.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_application = ApplicationModel(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


@app.get("/api/applications/", response_model=List[Application], tags=["applications"])
async def get_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applications = db.query(ApplicationModel).offset(skip).limit(limit).all()
    return applications


@app.get("/api/applications/{application_id}", response_model=ApplicationWithArtifacts, tags=["applications"])
async def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(ApplicationModel).filter(ApplicationModel.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@app.put("/api/applications/{application_id}", response_model=Application, tags=["applications"])
async def update_application(application_id: int, application: ApplicationUpdate, db: Session = Depends(get_db)):
    db_application = db.query(ApplicationModel).filter(ApplicationModel.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    update_data = application.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_application, key, value)
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


@app.delete("/api/applications/{application_id}", tags=["applications"])
async def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(ApplicationModel).filter(ApplicationModel.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return {"message": "Application deleted successfully"}