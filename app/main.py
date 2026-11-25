from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Dataset, DataRecord
from app.analytics.statistics import analyze_dataset

from app.database.connection import get_db
from app.upload import upload_dataset

app = FastAPI(
    title="STATZY DATA ANALYZER",
    description="AI-powered data analytics platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "application": "STATZY DATA ANALYZER",
        "status": "running",
        "message": "Welcome to Statzy!"
    }


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        content = await file.read()

        result = upload_dataset(
            db,
            content,
            file.filename
        )

        return result

    except (ValueError, UnicodeDecodeError) as error:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        import traceback

        db.rollback()

        print("\n========== STATZY UPLOAD ERROR ==========")
        traceback.print_exc()
        print("=========================================\n")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during upload."
        )

@app.get("/datasets/{dataset_id}/statistics")
def get_dataset_statistics(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    records = db.query(DataRecord).filter(
        DataRecord.dataset_id == dataset_id
    ).all()

    try:
        data = [
            record.record_data
            for record in records
        ]

        statistics = analyze_dataset(data)

        return {
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "statistics": statistics
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )