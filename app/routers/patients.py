from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse

from app.schemas import Patient, PatientUpdate
from app.storage import load_data, save_data

router = APIRouter(prefix="", tags=["patients"])


@router.get("/view")
def view():
    data = load_data()
    return data


@router.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="The ID of the patient to retrieve", examples=["P001"])
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@router.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="The attribute to sort patients by", examples=["age"]),
    order: str = Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending", examples=["asc"]),
):
    valid_fields = ["height", "weight", "age", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Choose from {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Choose 'asc' or 'desc'")

    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=(order == "desc"))
    return sorted_data


@router.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)


@router.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient_data = data[patient_id]
    patient_updated_data = patient_update.model_dump(exclude_unset=True)

    for key, value in patient_updated_data.items():
        existing_patient_data[key] = value

    updated_patient = Patient(id=patient_id, **existing_patient_data)
    data[patient_id] = updated_patient.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)


@router.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    save_data(data)
    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)
