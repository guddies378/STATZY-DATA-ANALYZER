from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Dataset, DataRecord
from app.analytics.analyzer import read_dataset
import pandas as pd
import numpy as np


def make_json_safe(value):
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating,)):
        return float(value)

    if isinstance(value, (np.bool_,)):
        return bool(value)

    if isinstance(value, (str, int, float, bool)):
        return value

    return str(value)


def upload_dataset(db: Session, file_content, filename):
    df = read_dataset(file_content, filename)

    # Generate a unique dataset name
    original_name = filename
    name = original_name
    counter = 1

    while db.query(Dataset).filter(
        Dataset.name == name
    ).first():
        name = f"{original_name.rsplit('.', 1)[0]} ({counter}).{original_name.rsplit('.', 1)[-1]}"
        counter += 1

    dataset = Dataset(
        name=name,
        description=f"Uploaded dataset with {len(df)} records",
        filename=filename
    )

    db.add(dataset)
    db.flush()

    records = df.to_dict(orient="records")

    for record in records:
        safe_record = {
            key: make_json_safe(value)
            for key, value in record.items()
        }

        db.add(
            DataRecord(
                dataset_id=dataset.id,
                record_data=safe_record
            )
        )

    db.commit()
    db.refresh(dataset)

    return {
        "message": "Dataset uploaded successfully!",
        "dataset_id": dataset.id,
        "dataset_name": dataset.name,
        "filename": filename,
        "total_records": len(df),
        "columns": list(df.columns)
    }