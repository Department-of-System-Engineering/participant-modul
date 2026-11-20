from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from enum import Enum

# Enums
class LanguageOccasion(str, Enum):
    EN = "en"
    HU = "hu"

class StatusOccasion(str, Enum):
    in_progress = "in_progress"
    completed = "completed"

class SexAllocation(str, Enum):
    male = "m"
    female = "f"

# Request
class StartDemographicsRequest(BaseModel):
    participant_pseudonym: str
    session_ref: str
    group_ref: str
    language: LanguageOccasion

# Response
class DemographicData(BaseModel):
    age: int
    sex: SexAllocation
    occupation: Optional[str] = None
    major: Optional[str] = None

class Demographic(BaseModel):
    id: UUID
    participant_pseudonym: str
    session_ref: str
    group_ref: str
    language: LanguageOccasion
    status: StatusOccasion = Field(default=StatusOccasion.in_progress)
    age: Optional[int] = None
    sex: Optional[SexAllocation] = None
    occupation: Optional[str] = None
    major: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    api_key_id: Optional[UUID] = None

class StartDemographicsResult(BaseModel):
    demographics_id: UUID
    status: StatusOccasion
    display_url: str

class DemographicsListResponse(BaseModel):
    group_ref: str
    demographics: list[Demographic]