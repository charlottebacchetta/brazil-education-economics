import pandas as pd
import os

base_dir = '/Users/charlottebacchetta/Desktop/Quant II Project'
years_to_check = [2007, 2008]

for year in years_to_check:
    folder_name = f'microdados_enem_{year}'
    file_name = f'MICRODADOS_ENEM_{year}.csv'
    file_path = os.path.join(base_dir, folder_name, file_name)

    print(f"\n🕵️ Vérification pour l'année {year}...")

    if not os.path.exists(file_path):
        print(f"❌ Fichier introuvable : {file_path}")
        continue

    try:
        print("📋 Lecture des premières lignes avec encoding='ISO-8859-1' et sep=';'...")
        df = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1', nrows=5)
        print(f"✅ Colonnes trouvées ({len(df.columns)}):")
        print(list(df.columns))
    except Exception as e1:
        print(f"⚠️ Échec avec ISO-8859-1 et ';' → {e1}")
        print("🔁 Tentative avec encoding='utf-8' et sep=','...")
        try:
            df = pd.read_csv(file_path, sep=',', encoding='utf-8', nrows=5)
            print(f"✅ Colonnes trouvées ({len(df.columns)}):")
            print(list(df.columns))
        except Exception as e2:
            print(f"❌ Échec aussi avec utf-8 → {e2}")
