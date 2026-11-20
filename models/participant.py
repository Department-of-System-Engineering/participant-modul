from pydantic import BaseModel
from datetime import datetime

class Participant(BaseModel):
    participant_pseudonym: str
    created_at: datetime