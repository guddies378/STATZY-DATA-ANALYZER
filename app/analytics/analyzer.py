import pandas as pd
from io import BytesIO


def read_dataset(file_content, filename):
    extension = filename.lower().split(".")[-1]

    if extension == "csv":
        df = pd.read_csv(BytesIO(file_content))

    elif extension in ["xlsx", "xls"]:
        df = pd.read_excel(BytesIO(file_content), engine="openpyxl")

    else:
        raise ValueError(
            "Unsupported file format. Upload CSV or Excel."
        )

    if df is None or df.empty:
        raise ValueError("The uploaded dataset is empty.")

    if len(df.columns) == 0:
        raise ValueError("The dataset has no columns.")

    return df