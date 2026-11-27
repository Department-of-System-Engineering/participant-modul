from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from enum import Enum

# Enums
class LanguageOccasion(str, Enum):
    """
    Supported languages for participant-facing screens.
    - EN: English
    - HU: Hungarian
    """
    EN = "en"
    HU = "hu"

class StatusOccasion(str, Enum):
    """
    Lifecycle status of a demographic data collection.
    - in_progress: the participant has not yet completed the form
    - completed: the participant has submitted their demographic data
    """
    in_progress = "in_progress"
    completed = "completed"

class SexAllocation(str, Enum):
    """
    Biological sex of the participant.
    - male: m
    - female: f
    """
    male = "m"
    female = "f"


# --- Request models (sent by the Experiment module) ---
class StartDemographicsRequest(BaseModel):
    """
    Request model for starting a demographic data collection.
    Called by the Experiment module after the participant confirms paper consent.
    - participant_pseudonym: unique identifier shared across all three modules
    - session_ref: the Experiment module's session ID
    - group_ref: the ethics approval number of the experiment
    - language: the language of the participant-facing form
    """
    participant_pseudonym: str
    session_ref: str
    group_ref: str
    language: LanguageOccasion


# --- Response models (returned by the backend) ---
class DemographicData(BaseModel):
    """
    The demographic data filled in by the participant.
    age and sex are required; occupation and major are optional.
    """
    age: int
    sex: SexAllocation
    occupation: Optional[str] = None
    major: Optional[str] = None

class Demographic(BaseModel):
    """
    Full demographic record response model.
    - age, sex, occupation, major are None until the participant completes the form
    - completed_at is None while the status is in_progress
    - api_key_id identifies which API key was used to start the data collection
    """
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
    """
    Response model returned after starting a demographic data collection.
    - demographics_id: used by the Experiment module to poll the status
    - display_url: the URL where the participant fills in their demographic data
    """
    demographics_id: UUID
    status: StatusOccasion
    display_url: str

class DemographicsListResponse(BaseModel):
    """
    Response model for listing all demographic records for a given group_ref.
    Used by the Experiment module to retrieve all demographics for one experiment.
    """
    group_ref: str
    demographics: list[Demographic]