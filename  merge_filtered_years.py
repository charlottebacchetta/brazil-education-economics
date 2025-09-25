import pandas as pd
import os

# Base path where all yearly filtered files are located
base_path = '/Users/charlottebacchetta/Desktop/Quant II Project/filtered_outputs'

# Final merged output file
output_file = os.path.join(base_path, 'merged_enem_SP_2009_2022.csv')

# Years to merge
years = list(range(2009, 2023))  # includes 2009 to 2022

# Initialize list to collect all DataFrames
all_dataframes = []

# Loop through years and load each filtered CSV
for year in years:
    file_path = os.path.join(base_path, str(year), f'filtered_enem_{year}_SP.csv')
    
    if os.path.exists(file_path):
        print(f"📥 Loading {file_path}...")
        try:
            df = pd.read_csv(file_path)
            all_dataframes.append(df)
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")
    else:
        print(f"❌ File not found for {year}: skipping.")

# Merge all DataFrames
if all_dataframes:
    merged_df = pd.concat(all_dataframes, ignore_index=True)
    merged_df.to_csv(output_file, index=False)
    print(f"\n✅ Merged file saved to: {output_file}")
else:
    print("\n⚠️ No data found to merge.")
