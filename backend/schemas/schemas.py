from pydantic import BaseModel, HttpUrl
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class LaneEnum(str, Enum):
    software_engineering = "software_engineering"
    devops = "devops"
    security = "security"


class ArtifactTypeEnum(str, Enum):
    resume = "resume"
    bullets = "bullets"
    cover_letter = "cover_letter"


class JobStatusEnum(str, Enum):
    interested = "interested"
    applied = "applied"
    rejected = "rejected"
    offer = "offer"
    negotiating = "negotiating"


class ApplicationResponseEnum(str, Enum):
    no_response = "no_response"
    rejected = "rejected"
    interview = "interview"
    offer = "offer"




class FontSizeEnum(str, Enum):
    size_12pt = "12pt"
    size_10pt = "10pt"


# Role Schemas
class RoleBase(BaseModel):
    lane: LaneEnum
    core_skills: str
    notes: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    lane: Optional[LaneEnum] = None
    core_skills: Optional[str] = None
    notes: Optional[str] = None


class Role(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Artifact Metric Schemas
class ArtifactMetricBase(BaseModel):
    name: str
    notes: Optional[str] = None
    active: bool = True
    ai_generated: bool = False   
    bullet_points: Optional[bool] = None
    artifact_format_details: Optional[str] = None
    font_size: Optional[FontSizeEnum] = None


class ArtifactMetricCreate(ArtifactMetricBase):
    pass


class ArtifactMetricUpdate(BaseModel):
    name: Optional[str] = None
    notes: Optional[str] = None
    active: Optional[bool] = None
    ai_generated: Optional[bool] = None    
    bullet_points: Optional[bool] = None
    artifact_format_details: Optional[str] = None
    font_size: Optional[FontSizeEnum] = None


class ArtifactMetric(ArtifactMetricBase):
    id: int
    artifact_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Artifact Schemas
class ArtifactBase(BaseModel):
    type: ArtifactTypeEnum
    version_name: str
    location: Optional[str] = None
    notes: Optional[str] = None
    active: bool = True


class ArtifactCreate(ArtifactBase):
    pass


class ArtifactUpdate(BaseModel):
    type: Optional[ArtifactTypeEnum] = None
    version_name: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    active: Optional[bool] = None


class Artifact(ArtifactBase):
    id: int
    created: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    metrics: List[ArtifactMetric] = []

    class Config:
        from_attributes = True


class ArtifactWithMetrics(Artifact):
    metrics: List[ArtifactMetric]


# Job Schemas
class JobBase(BaseModel):
    company: str
    title: str
    posting_url: Optional[str] = None
    required_skills: Optional[str] = None
    date_found: datetime
    status: JobStatusEnum = JobStatusEnum.interested
    fit_score: Optional[int] = None
    notes: Optional[str] = None
    role_id: int


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    posting_url: Optional[str] = None
    required_skills: Optional[str] = None
    date_found: Optional[datetime] = None
    status: Optional[JobStatusEnum] = None
    fit_score: Optional[int] = None
    notes: Optional[str] = None
    role_id: Optional[int] = None


class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobWithApplications(Job):
    applications: List['Application'] = []


# Application Schemas
class ApplicationBase(BaseModel):
    job_id: int
    date_sent: datetime
    contact: Optional[str] = None
    response: Optional[ApplicationResponseEnum] = None
    next_action_date: Optional[date] = None
    notes: Optional[str] = None
    active: bool = True


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    job_id: Optional[int] = None
    date_sent: Optional[datetime] = None
    contact: Optional[str] = None
    response: Optional[ApplicationResponseEnum] = None
    next_action_date: Optional[date] = None
    notes: Optional[str] = None
    active: Optional[bool] = None


class Application(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ApplicationWithArtifacts(Application):
    artifacts: List[Artifact] = []


# Update forward references
JobWithApplications.model_rebuild()
ApplicationWithArtifacts.model_rebuild()