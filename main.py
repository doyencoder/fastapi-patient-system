from fastapi import FastAPI

from app.routers.patients import router as patients_router

app = FastAPI(title="Patient Management System API")


@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional Patient Management System API using FastAPI."}


app.include_router(patients_router)

