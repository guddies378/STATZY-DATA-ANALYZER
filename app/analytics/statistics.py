import pandas as pd


def analyze_dataset(records):
    if not records:
        raise ValueError("This dataset contains no records.")

    df = pd.DataFrame(records)

    results = {
        "total_records": int(len(df)),
        "total_columns": int(len(df.columns)),
        "columns": {},
        "correlations": {}
    }

    numeric_columns = []

    for column in df.columns:
        series = df[column]
        non_missing = series.dropna()

        numeric_series = pd.to_numeric(
            non_missing,
            errors="coerce"
        )

        is_numeric = (
            len(non_missing) > 0
            and numeric_series.notna().all()
        )

        column_result = {
            "data_type": "numeric" if is_numeric else "categorical",
            "missing_values": int(series.isna().sum()),
            "unique_values": int(series.nunique())
        }

        if is_numeric:
            numeric_columns.append(column)

            values = numeric_series

            modes = values.mode().tolist()

            column_result.update({
                "count": int(values.count()),
                "mean": float(values.mean()),
                "median": float(values.median()),
                "mode": [float(value) for value in modes],
                "minimum": float(values.min()),
                "maximum": float(values.max()),
                "standard_deviation": (
                    float(values.std())
                    if len(values) > 1 else None
                ),
                "variance": (
                    float(values.var())
                    if len(values) > 1 else None
                ),
                "sum": float(values.sum()),
                "quartiles": {
                    "25%": float(values.quantile(0.25)),
                    "50%": float(values.quantile(0.50)),
                    "75%": float(values.quantile(0.75))
                }
            })

        else:
            modes = non_missing.mode().tolist()

            column_result.update({
                "count": int(non_missing.count()),
                "mode": [str(value) for value in modes],
                "top_values": [
                    {
                        "value": str(value),
                        "count": int(count)
                    }
                    for value, count in
                    non_missing.value_counts().head(5).items()
                ]
            })

        results["columns"][column] = column_result

    # Calculate correlations between numeric columns
    if len(numeric_columns) >= 2:
        numeric_df = df[numeric_columns].apply(
            pd.to_numeric,
            errors="coerce"
        )

        correlation_df = numeric_df.corr()

        results["correlations"] = {
            column: {
                other_column: (
                    None if pd.isna(value) else float(value)
                )
                for other_column, value in row.items()
            }
            for column, row in correlation_df.iterrows()
        }

    return results