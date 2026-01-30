from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="Unique identifier for the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Full name of the patient", examples=["John Doe"])]
    city: Annotated[str, Field(..., description="City of residence", examples=["Pune"])]
    age: Annotated[int, Field(..., gt=0, lt=100, description="Age of the patient", examples=[30])]
    gender: Annotated[
        Literal["Male", "Female", "Other"],
        Field(..., description="Gender of the patient", examples=["Male"])
    ]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters", examples=[1.75])]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms", examples=[70.2])]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
     
class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(None, description="Full name of the patient", examples=["John Doe"])]
    city: Annotated[Optional[str], Field(None, description="City of residence", examples=["Pune"])]
    age: Annotated[Optional[int], Field(None, gt=0, lt=100, description="Age of the patient", examples=[30])]
    gender: Annotated[
        Literal["Male", "Female", "Other"],
        Field(None, description="Gender of the patient", examples=["Male"])
    ]
    height: Annotated[Optional[float], Field(None, gt=0, description="Height of the patient in meters", examples=[1.75])]
    weight: Annotated[Optional[float], Field(None, gt=0, description="Weight of the patient in kilograms", examples=[70.2])]

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
        
    return data

def save_data(data):
    with open("patients.json", "w") as file:
        json.dump(data, file)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional Patient Management System API using FastAPI."}

@app.get("/view")
def view():
    data = load_data()
    
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", examples="P001")):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="The attribute to sort patients by", examples="age"), order: str = Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending", examples="asc")):
    
    valid_fields = ["height", "weight", "age", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Choose from {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Choose 'asc' or 'desc'")
    
    data = load_data()

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=(order == "desc"))

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #check if patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    #if not, add new patient to database
    data[patient.id] = patient.model_dump(exclude={'id'})

    #save updated data back to file
    save_data(data)

    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_data = data[patient_id]
    patient_updated_data = patient_update.model_dump(exclude_unset=True)

    for key, value in patient_updated_data.items():
        existing_patient_data[key] = value

    exitng_patient = Patient(id=patient_id, **existing_patient_data)
    data[patient_id] = exitng_patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    save_data(data)
    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)

