import pandas as pd

INPUT_CSV = "data\CitizenLab_Senegal_KnowledgeBase_v1.CSV"
OUTPUT_CSV = "data\cleaned.csv"

df = pd.read_csv(INPUT_CSV)

# Normalisation colonnes
df.columns = [c.strip().lower() for c in df.columns]



# Nettoyage
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Nettoyage texte
df["question"] = df["question"].str.strip()
df["answer"] = df["answer"].str.strip()

df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

print(f"✅ CSV nettoyé : {len(df)} lignes")
