from openpyxl import load_workbook

file_path = "sample_sales.xlsx"

workbook = load_workbook(file_path, data_only=True)

print("\nEXCEL WORKSHEET NAMES:")
print(workbook.sheetnames)

for sheet in workbook.worksheets:
    print(f"\nWorksheet: {sheet.title}")
    print(f"Rows: {sheet.max_row}")
    print(f"Columns: {sheet.max_column}")

    for row in sheet.iter_rows(min_row=1, max_row=min(sheet.max_row, 6), values_only=True):
        print(row)