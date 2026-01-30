from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field, computed_field


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique identifier for the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Full name of the patient", examples=["John Doe"])]
    city: Annotated[str, Field(..., description="City of residence", examples=["Pune"])]
    age: Annotated[int, Field(..., gt=0, lt=100, description="Age of the patient", examples=[30])]
    gender: Annotated[
        Literal["Male", "Female", "Other"],
        Field(..., description="Gender of the patient", examples=["Male"]),
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
        if 18.5 <= self.bmi < 25:
            return "Normal"
        if 25 <= self.bmi < 30:
            return "Overweight"
        return "Obese"


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, description="Full name of the patient", examples=["John Doe"])]
    city: Annotated[Optional[str], Field(None, description="City of residence", examples=["Pune"])]
    age: Annotated[Optional[int], Field(None, gt=0, lt=100, description="Age of the patient", examples=[30])]
    gender: Annotated[
        Literal["Male", "Female", "Other"],
        Field(None, description="Gender of the patient", examples=["Male"]),
    ]
    height: Annotated[Optional[float], Field(None, gt=0, description="Height of the patient in meters", examples=[1.75])]
    weight: Annotated[Optional[float], Field(None, gt=0, description="Weight of the patient in kilograms", examples=[70.2])]
