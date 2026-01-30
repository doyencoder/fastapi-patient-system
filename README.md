# Patient Management System API

A lightweight FastAPI service that manages patient records stored in a local JSON file. Each patient includes BMI and a verdict category derived from height and weight ($BMI = \frac{weight}{height^2}$).

## Prerequisites
- Python 3.10+
- `pip` for installing dependencies

## Setup
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```
2. Ensure the seed data file exists (included): `patients.json`.

## Run the server
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## Data store
- Records are persisted in `patients.json` as a simple key/value store keyed by patient ID.
- BMI and verdict are recomputed when creating or updating a patient.

## Schemas
- **Patient** (used for create):
  - `id` (string, required)
  - `name` (string, required)
  - `city` (string, required)
  - `age` (int, required, 1-99)
  - `gender` (enum: Male | Female | Other, case-sensitive)
  - `height` (float, meters, >0)
  - `weight` (float, kg, >0)
  - `bmi` (computed: `weight / height^2`, rounded to 2 decimals)
  - `verdict` (computed from BMI: Underweight, Normal, Overweight, Obese)
- **PatientUpdate** (used for edit): same fields as `Patient` but all optional and without `id`; `bmi` and `verdict` are recomputed after validation.

## API endpoints
- `GET /` – Health/message check.
- `GET /about` – Service description.
- `GET /view` – Return all patients.
- `GET /patient/{patient_id}` – Return a single patient by ID.
- `GET /sort?sort_by=height|weight|age|bmi&order=asc|desc` – Sorted list of patients.
- `POST /create` – Create a patient.
- `PUT /edit/{patient_id}` – Update an existing patient (partial updates supported).
- `DELETE /delete/{patient_id}` – Delete a patient by ID.

## Example requests
- Create a patient:
  ```bash
  curl -X POST http://127.0.0.1:8000/create \
    -H "Content-Type: application/json" \
    -d '{
      "id": "P010",
      "name": "Jane Doe",
      "city": "Pune",
      "age": 29,
      "gender": "Female",
      "height": 1.68,
      "weight": 62
    }'
  ```
- Update a patient:
  ```bash
  curl -X PUT http://127.0.0.1:8000/edit/P010 \
    -H "Content-Type: application/json" \
    -d '{
      "city": "Mumbai",
      "weight": 64
    }'
  ```
- Sort patients by BMI descending:
  ```bash
  curl "http://127.0.0.1:8000/sort?sort_by=bmi&order=desc"
  ```
- Fetch a patient:
  ```bash
  curl http://127.0.0.1:8000/patient/P002
  ```
- Delete a patient:
  ```bash
  curl -X DELETE http://127.0.0.1:8000/delete/P010
  ```

## Notes
- Valid genders are `Male`, `Female`, or `Other` (case-sensitive).
- Age is constrained to 1–99; height and weight must be positive numbers.
- For production use, replace the JSON file store with a database and add authentication.
