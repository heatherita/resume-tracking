from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class LaneEnum(str, enum.Enum):
    software_engineering = "software_engineering"
    devops = "devops"
    security = "security"


class ArtifactTypeEnum(str, enum.Enum):
    resume = "resume"
    cover_letter = "cover_letter"


class JobStatusEnum(str, enum.Enum):
    interested = "interested"
    applied = "applied"
    rejected = "rejected"
    offer = "offer"
    negotiating = "negotiating"


class ApplicationResponseEnum(str, enum.Enum):
    no_response = "no_response"
    rejected = "rejected"
    interview = "interview"
    offer = "offer"

class TruthLevelEnum(str, enum.Enum):
    low = "low"
    med = "med"
    high = "high"


class PromptStrictnessEnum(str, enum.Enum):
    low = "low"
    med = "med"
    high = "high"

class FontSizeEnum(str, enum.Enum):
    size_12pt = "12pt"
    size_10pt = "10pt"

class SectionTypeEnum(str, enum.Enum):
    header = "header"
    text = "text"
    bullets = "bullets"

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    lane = Column(Enum(LaneEnum), nullable=False)
    core_skills = Column(Text, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    jobs = relationship("Job", lazy="selectin", back_populates="role")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    posting_url = Column(String)
    required_skills = Column(Text)
    date_found = Column(Date)
    status = Column(Enum(JobStatusEnum), nullable=False, default=JobStatusEnum.interested)
    fit_score = Column(Integer)
    notes = Column(Text)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    role = relationship("Role", back_populates="jobs")
    applications = relationship("Application", back_populates="job", lazy="selectin", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    date_sent = Column(Date)
    contact = Column(String)
    response = Column(Enum(ApplicationResponseEnum))
    next_action_date = Column(Date)
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    job = relationship("Job", back_populates="applications")
    artifacts = relationship("Artifact", back_populates="applications", lazy="selectin", cascade="all, delete-orphan")


class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    type = Column(Enum(ArtifactTypeEnum), nullable=False)
    version_name = Column(String, nullable=False)
    location = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    sections = relationship("Section", secondary="artifact_sections", back_populates="artifacts", lazy="selectin")
    metrics = relationship("ArtifactMetric", back_populates="artifact", lazy="selectin", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="artifacts")
    
class ArtifactMetric(Base):
    __tablename__ = "artifact_metrics"

    id = Column(Integer, primary_key=True, index=True)
    artifact_id = Column(Integer, ForeignKey("artifacts.id"), nullable=False)
    name = Column(String, nullable=False)
    notes = Column(Text)
    active = Column(Boolean, default=True)
    truth_level = Column(Enum(TruthLevelEnum), info="Level of outright bending the truth found intruth the artifact")
    prompt_strictness = Column(Enum(PromptStrictnessEnum), info="Level of strictness in the task prompt in adhering to source documents")
    ai_generated = Column(Boolean, default=False)
    bullet_points = Column(Boolean, info="Whether the artifact contains bullet points for experiences")
    artifact_format_details = Column(String, info="Format details: two-column/colors_used/headshot_used/serif_font")
    font_size = Column(Enum(FontSizeEnum))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    artifact = relationship("Artifact", back_populates="metrics")


class Section(Base):
    __tablename__ = "sections" 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(SectionTypeEnum), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    artifacts = relationship("Artifact", secondary="artifact_sections", back_populates="sections", lazy="selectin")


# Association table for many-to-many relationship between Artifacts and Sections
artifact_sections = Table(
    "artifact_sections",
    Base.metadata,
    Column("artifact_id", Integer, ForeignKey("artifacts.id"), primary_key=True),
    Column("section_id", Integer, ForeignKey("sections.id"), primary_key=True),
    Column("section_order", Integer, nullable=False, server_default="1"),
)
