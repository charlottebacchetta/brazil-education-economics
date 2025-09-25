import pandas as pd
import os

# Base folder path
base_dir = '/Users/charlottebacchetta/Desktop/Quant II Project'
output_base = os.path.join(base_dir, 'filtered_outputs')

# Columns to keep (ENEM post-2009 structure)
columns_to_keep = [
    'NU_ANO',
    'NO_MUNICIPIO_PROVA',
    'SG_UF_PROVA',
    'NU_NOTA_CN',
    'NU_NOTA_CH',
    'NU_NOTA_LC',
    'NU_NOTA_MT'
]

# Only process 2014 and 2016
selected_years = [2021, 2022]

for year in selected_years:
    folder_name = f'microdados_enem_{year}'
    file_name = f'MICRODADOS_ENEM_{year}.csv'
    file_path = os.path.join(base_dir, folder_name, file_name)

    if os.path.exists(file_path):
        print(f"\n📘 Processing year {year}...")

        try:
            # Read only selected columns
            df = pd.read_csv(file_path, usecols=columns_to_keep, encoding='ISO-8859-1', sep=';')

            # Filter for SG_UF_PROVA = 'SP'
            df_sp = df[df['SG_UF_PROVA'] == 'SP']

            # Create output folder if not exists
            year_output_dir = os.path.join(output_base, str(year))
            os.makedirs(year_output_dir, exist_ok=True)

            # Save filtered output
            output_file = os.path.join(year_output_dir, f'filtered_enem_{year}_SP.csv')
            df_sp.to_csv(output_file, index=False)

            print(f"✅ Saved: {output_file}")
        except Exception as e:
            print(f"⚠️ Error processing {file_name}: {e}")
    else:
        print(f"❌ File not found: {file_path}")
