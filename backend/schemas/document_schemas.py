from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from enum import Enum


class CoverLetterRequest(BaseModel):
    application_id: int
    username: str