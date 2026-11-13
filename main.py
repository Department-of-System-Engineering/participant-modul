from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal, Optional

app = FastAPI()

class StartDemographicsRequest(BaseModel):
    participant_pseudonym: str           # required
    session_ref: str                     # required
    group_ref: str                       # required
    language: Literal["hu", "en"]        # required, only "hu" or "en" allowed


class DemographicData(BaseModel):
    age: int                             # required
    sex: Literal["m", "f"]              # required, only "m" or "f" allowed
    occupation: Optional[str] = None    # optional — defaults to None if missing
    major: Optional[str] = None         # optional


# --- Endpoints ---

@app.get("/hello/{name}")
def say_hello_to(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/demographics/{id}")
def get_demographics(id: int):
    # Database comes next
    return {
        "id": id,
        "age": 25,
        "sex": "m",
        "occupation": "Software Engineer",
        "major": "Computer Science"
    }

@app.get("/demographics?group_ref={group_ref}")
def get_demographics_by_group(group_ref: str):
    # Database comes next
    return {
        "group_ref": group_ref,
        "participants": [
            {"id": 1, "age": 25, "sex": "m", "occupation": "Software Engineer", "major": "Computer Science"},
            {"id": 2, "age": 30, "sex": "f", "occupation": "Data Scientist", "major": "Statistics"}
        ]
    }

@app.post("/demographics")
def start_demographics(req: StartDemographicsRequest):

    # Database comes next
    return {
        "received": req.model_dump(),
        "message": "Data looks good! Database coming in the next step."
    }