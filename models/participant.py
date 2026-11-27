from pydantic import BaseModel
from datetime import datetime


class Participant(BaseModel):
    """
    Represents a participant in the system.
    - participant_pseudonym: unique identifier shared across all three modules.
      It is set by the researcher and never changes.
    - created_at: the timestamp when the participant was first registered.
      A participant is registered automatically on their first demographic data collection.
    """
    participant_pseudonym: str
    created_at: datetime