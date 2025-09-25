import pandas as pd
import os

# 📂 Paths
original_base = '/Users/charlottebacchetta/Desktop/Quant II Project/Original Datasets'
expenditure_file = '/Users/charlottebacchetta/Desktop/Quant II Project/Independent Variables datasets/Public Expenditure on Education per City SP.xlsx'
output_folder = '/Users/charlottebacchetta/Desktop/Quant II Project/filtered_outputs'
output_file = os.path.join(output_folder, 'education_expenditure_per_student_per_city_2009_2022.csv')

# 📜 Columns to keep from ENEM
columns_of_interest = [
    'NU_ANO',
    'NO_MUNICIPIO_PROVA',
    'SG_UF_PROVA'
]

# 📅 Years to process
years = list(range(2009, 2023))  # 2009 to 2022

# 🔹 Step 1: Compute number of ENEM students per city and year
enem_counts = []

for year in years:
    print(f"📥 Loading ENEM data for {year}...")

    file_path = os.path.join(original_base, f'microdados_enem_{year}', f'MICRODADOS_ENEM_{year}.csv')
    
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1', usecols=columns_of_interest)
            df_sp = df[df['SG_UF_PROVA'] == 'SP']  # Only São Paulo students
            counts = df_sp.groupby(['NU_ANO', 'NO_MUNICIPIO_PROVA']).size().reset_index(name='NB_STUDENTS')
            enem_counts.append(counts)
            print(f"✅ Students counted for {year}: {counts.shape[0]} cities")
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    else:
        print(f"❌ ENEM file not found for {year}")

# Concatenate all years
enem_student_counts = pd.concat(enem_counts, ignore_index=True)

# 🔹 Step 2: Load Public Education Expenditure data
print("\n📥 Loading Public Expenditure data...")
expenditure_df = pd.read_excel(expenditure_file)

# 🔥 Rename columns properly
expenditure_df.rename(columns={
    'Ano': 'NU_ANO',
    'Município': 'NO_MUNICIPIO_PROVA',
    'Valor aplicado em educação (R$)': 'EXPENDITURE'
}, inplace=True)

print(f"✅ Public Expenditure data loaded: {expenditure_df.shape[0]} rows")

# 🔹 Step 3: Merge ENEM counts and Expenditure data
print("\n🔗 Merging datasets...")

merged_df = pd.merge(
    enem_student_counts,
    expenditure_df,
    how='inner',
    on=['NU_ANO', 'NO_MUNICIPIO_PROVA']
)

# 🔹 Step 4: Calculate Expenditure per Student
print("\n📊 Calculating Education Expenditure per ENEM Student...")
merged_df['EXPENDITURE_PER_STUDENT'] = merged_df['EXPENDITURE'] / merged_df['NB_STUDENTS']

# 🔹 Step 5: Save final dataset
os.makedirs(output_folder, exist_ok=True)
merged_df.to_csv(output_file, index=False)

print(f"\n✅ Final dataset saved to: {output_file}")
