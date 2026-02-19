from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from enum import Enum


class LaneEnum(str, Enum):
    software_engineering = "software_engineering"
    devops = "devops"
    security = "security"


class ArtifactTypeEnum(str, Enum):
    resume = "resume"
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

class TruthLevelEnum(str, Enum):
    low = "low"
    med = "med"
    high = "high"


class PromptStrictnessEnum(str, Enum):
    low = "low"
    med = "med"
    high = "high"


class FontSizeEnum(str, Enum):
    size_12pt = "12pt"
    size_10pt = "10pt"


class ArtifactFormatDetailsEnum(str, Enum):
    two_column = "two-column"
    colors_used = "colors_used"
    headshot_used = "headshot_used"
    serif_font = "serif_font"


class SectionTypeEnum(str, Enum):
    header = "header"
    text = "text"
    bullets = "bullets"


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


class RoleOut(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True






# Job Schemas
class JobBase(BaseModel):
    company: str
    title: str
    posting_url: Optional[str] = None
    required_skills: Optional[str] = None
    date_found: Optional[date] = None
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
    date_found: Optional[date] = None
    status: Optional[JobStatusEnum] = None
    fit_score: Optional[int] = None
    notes: Optional[str] = None
    role_id: Optional[int] = None


class JobOut(JobBase):
    id: int
    role: Optional[RoleOut] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Application Schemas
class ApplicationBase(BaseModel):
    job_id: int
    date_sent: Optional[date] = None
    contact: Optional[str] = None
    response: Optional[ApplicationResponseEnum] = None
    next_action_date: Optional[date] = None
    notes: Optional[str] = None
    active: bool = True


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    job_id: Optional[int] = None
    date_sent: Optional[date] = None
    contact: Optional[str] = None
    response: Optional[ApplicationResponseEnum] = None
    next_action_date: Optional[date] = None
    notes: Optional[str] = None
    active: Optional[bool] = None

class ApplicationOut(ApplicationBase):
    id: int
    job: Optional[JobOut] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True



# Artifact Schemas
class ArtifactBase(BaseModel):
    type: ArtifactTypeEnum
    version_name: str
    location: Optional[str] = None
    application_id: int
    notes: Optional[str] = None
    active: bool = True


class ArtifactCreate(ArtifactBase):
    pass


class ArtifactUpdate(BaseModel):
    type: Optional[ArtifactTypeEnum] = None
    version_name: Optional[str] = None
    location: Optional[str] = None
    application_id: Optional[int] = None
    notes: Optional[str] = None
    active: Optional[bool] = None


class ArtifactOut(ArtifactBase):
    id: int
    application: Optional[ApplicationOut] = Field(default=None, validation_alias="applications")
    created: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SectionBase(BaseModel):
    name: str
    type: SectionTypeEnum
    content: str
    order: int


class SectionCreate(SectionBase):
    pass


class SectionUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[SectionTypeEnum] = None
    content: Optional[str] = None
    order: Optional[int] = None


class SectionOut(SectionBase):
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
    truth_level: Optional[TruthLevelEnum] = None
    prompt_strictness: Optional[PromptStrictnessEnum] = None
    bullet_points: Optional[bool] = None
    artifact_format_details: Optional[ArtifactFormatDetailsEnum] = None
    font_size: Optional[FontSizeEnum] = None


class ArtifactMetricCreate(ArtifactMetricBase):
    pass


class ArtifactMetricUpdate(BaseModel):
    name: Optional[str] = None
    notes: Optional[str] = None
    active: Optional[bool] = None
    ai_generated: Optional[bool] = None 
    truth_level: Optional[TruthLevelEnum] = None
    prompt_strictness: Optional[PromptStrictnessEnum] = None   
    bullet_points: Optional[bool] = None
    artifact_format_details: Optional[ArtifactFormatDetailsEnum] = None
    font_size: Optional[FontSizeEnum] = None


class ArtifactMetricOut(ArtifactMetricBase):
    id: int
    artifact_id: int
    artifact: Optional[ArtifactOut] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Update forward references
ArtifactMetricOut.model_rebuild()
