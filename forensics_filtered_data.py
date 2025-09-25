import pandas as pd
import os

# Base folders
original_base = '/Users/charlottebacchetta/Desktop/Quant II Project/Original Datasets'
output_base = '/Users/charlottebacchetta/Desktop/Quant II Project/filtered_outputs/yearly_city_averages'

# Columns to keep
columns_of_interest = [
    'NU_ANO',
    'NO_MUNICIPIO_PROVA',
    'SG_UF_PROVA',
    'NU_NOTA_CN',
    'NU_NOTA_CH',
    'NU_NOTA_LC',
    'NU_NOTA_MT'
]

# Make sure the output folder exists
os.makedirs(output_base, exist_ok=True)

# Years to process
years = list(range(2009, 2023))  # 2009 to 2022

for year in years:
    print(f"\n📥 Processing year {year}...")

    file_path = os.path.join(original_base, f'microdados_enem_{year}', f'MICRODADOS_ENEM_{year}.csv')

    if os.path.exists(file_path):
        try:
            # Load data
            df = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1', usecols=columns_of_interest)

            # Filter for São Paulo
            df_sp = df[df['SG_UF_PROVA'] == 'SP']

            print(f"✅ São Paulo schools for {year}: {df_sp.shape[0]}")

            # Calculate average scores per city (ignore NaN automatically)
            score_columns = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT']
            city_avg_scores = df_sp.groupby('NO_MUNICIPIO_PROVA')[score_columns].mean()

            # Count number of schools per city
            city_school_counts = df_sp.groupby('NO_MUNICIPIO_PROVA').size().reset_index(name='NB_SCHOOLS')

            # Merge averages and counts
            final_city_table = city_avg_scores.reset_index().merge(city_school_counts, on='NO_MUNICIPIO_PROVA')

            # Add the year as a new column
            final_city_table['NU_ANO'] = year

            # Save output
            output_file = os.path.join(output_base, f'avg_scores_and_nb_schools_per_city_{year}.csv')
            final_city_table.to_csv(output_file, index=False)

            print(f"💾 Saved for year {year}: {output_file}")

        except Exception as e:
            print(f"❌ Error processing {year}: {e}")
    else:
        print(f"❌ File not found for {year}!")
