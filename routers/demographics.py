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
import json

router = APIRouter(prefix="/demographics", tags=["demographics"])

@router.get("/{id}", response_model=Demographic)
async def get_demographic_by_id(id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM demographics WHERE id = %s", (id))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Demographic not found")
        return dict(row)

@router.get("/", response_model=DemographicsListResponse)
async def list_demographics_by_group(group_ref: str):
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
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO participants (participant_pseudonym) VALUES (%s) ON CONFLICT DO NOTHING", (data.participant_pseudonym,))
        cursor.execute("INSERT INTO demographics (participant_pseudonym, session_ref, group_ref, language) VALUES (%s, %s, %s, %s) RETURNING id", (data.participant_pseudonym, data.session_ref, data.group_ref, data.language.value))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=500, detail="Failed to create demographics")
        demographics_id = row[0]
        display_url = f"http://localhost:8090/d/{demographics_id}"
        return StartDemographicsResult(
            demographics_id=demographics_id,
            status=StatusOccasion.in_progress,
            display_url=display_url
        )