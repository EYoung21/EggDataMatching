import pandas as pd

# Read the Excel file
excel_file = "HSI egg data_Poultry farm exp_Master file.xlsx"
df = pd.read_excel(excel_file)

# Save as CSV
csv_file = "HSI_egg_data.csv"
df.to_csv(csv_file, index=False)

print(f"Converted {excel_file} to {csv_file}") 