import pandas as pd
import re

# ================================
# CONFIGURATION
# ================================
INPUT_CSV = "rag_pipeline/data/raw/CitizenLab_Senegal_KnowledgeBase_v1.CSV"
OUTPUT_CSV = "rag_pipeline/data/clean/citizenlab_rag_clean.csv"

REQUIRED_COLUMNS = [
    "theme",
    "sous_theme",
    "question",
    "reponse",
    "source"
]

# ================================
# FONCTIONS DE NETTOYAGE
# ================================
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = text.strip()
    text = re.sub(r"\s+", " ", text)          # espaces multiples
    text = re.sub(r"[“”]", '"', text)          # guillemets typographiques
    text = re.sub(r"[’]", "'", text)
    return text

# ================================
# CHARGEMENT
# ================================
df = pd.read_csv(INPUT_CSV)

print(f"Lignes chargées : {len(df)}")

# ================================
# VALIDATION STRUCTURE
# ================================
missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
if missing_cols:
    raise ValueError(f"❌ Colonnes manquantes : {missing_cols}")

# ================================
# NETTOYAGE
# ================================
for col in REQUIRED_COLUMNS:
    df[col] = df[col].apply(clean_text)

# Supprimer lignes vides
df = df[
    (df["question"] != "") &
    (df["reponse"] != "")
]

# ================================
# DÉDUPLICATION
# ================================
df_before = len(df)

df = df.drop_duplicates(
    subset=["question", "reponse"],
    keep="first"
)

df_after = len(df)
print(f"🧹 Doublons supprimés : {df_before - df_after}")

# ================================
# NORMALISATION
# ================================
df["question_norm"] = df["question"].str.lower()
df = df.drop_duplicates(subset=["question_norm"])
df = df.drop(columns=["question_norm"])

# ================================
# CONTRÔLES QUALITÉ
# ================================
print("📊 Résumé qualité :")
print(f"- Total Q/R : {len(df)}")
print(f"- Thèmes uniques : {df['theme'].nunique()}")
print(f"- Sous-thèmes uniques : {df['sous_theme'].nunique()}")

# ================================
# EXPORT FINAL
# ================================
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

print(f"✅ CSV propre exporté : {OUTPUT_CSV}")
