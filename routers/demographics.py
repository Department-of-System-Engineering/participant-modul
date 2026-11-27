from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from database import get_db
from models.demographic import (
    Demographic,
    StartDemographicsRequest,
    StartDemographicsResult,
    DemographicsListResponse,
    StatusOccasion
)
from uuid import UUID

router = APIRouter(prefix="/demographics", tags=["demographics"])


@router.get("/{id}", response_model=Demographic, responses={404: {"description": "Demographic not found"}})
async def get_demographic_by_id(id: str):
    """
    Returns a single demographic record by its UUID.
    Raises 404 if the record does not exist.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM demographics WHERE id = %s", (id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Demographic not found")
        return dict(row)


@router.get("/", response_model=DemographicsListResponse)
async def list_demographics_by_group(group_ref: str):
    """
    Returns all demographic records for a given group_ref.
    The group_ref corresponds to the ethics approval number of an experiment.
    Used by the Experiment module to retrieve all demographics for one experiment.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM demographics WHERE group_ref = %s", (group_ref,))
        rows = cursor.fetchall()
        return DemographicsListResponse(
            group_ref=group_ref,
            demographics=[Demographic(**dict(row)) for row in rows]
        )


@router.post("/", response_model=StartDemographicsResult, status_code=201)
async def start_demographics(data: StartDemographicsRequest):
    """
    Starts a new demographic data collection for a participant.
    Called by the Experiment module after the participant confirms paper consent.

    - If the participant_pseudonym is new, the participant is added to the participants table.
    - If the participant already exists, the new record is linked to the existing participant.
    - Returns the demographics_id and a display_url where the participant fills in their data.

    Raises 500 if the demographic record could not be created.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        # Add participant if not already registered
        cursor.execute("INSERT INTO participants (participant_pseudonym) VALUES (%s) ON CONFLICT DO NOTHING", (data.participant_pseudonym,))
        # Create the demographic record
        cursor.execute("INSERT INTO demographics (participant_pseudonym, session_ref, group_ref, language) VALUES (%s, %s, %s, %s) RETURNING id", (data.participant_pseudonym, data.session_ref, data.group_ref, data.language.value))
        row = dict(cursor.fetchone() or {})
        demographics_id = UUID(str(row["id"]))  # Convert string to UUID
        display_url = f"http://localhost:8090/d/{demographics_id}"
        return StartDemographicsResult(
            demographics_id=demographics_id,
            status=StatusOccasion.in_progress,
            display_url=display_url
        )