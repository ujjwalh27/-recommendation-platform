import pandas as pd
import re

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("datasets/processed/videos.csv")

# -----------------------------
# Text Cleaning Function
# -----------------------------
def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Remove emojis & non-ascii
    text = text.encode("ascii", "ignore").decode()

    # Remove punctuation
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.lower().strip()

# -----------------------------
# Clean Columns
# -----------------------------
df["caption"] = df["caption"].fillna("").apply(clean_text)
df["hashtags"] = df["hashtags"].fillna("").apply(clean_text)
df["creator_name"] = df["creator_name"].fillna("").apply(clean_text)
df["music_name"] = df["music_name"].fillna("").apply(clean_text)

# -----------------------------
# Combine Important Features
# -----------------------------
df["combined_text"] = (
    df["caption"]
    + " "
    + df["hashtags"]
    + " music "
    + df["music_name"]
    + " creator "
    + df["creator_name"]
)

# Remove extra spaces
df["combined_text"] = df["combined_text"].str.replace(r"\s+", " ", regex=True)

# -----------------------------
# Save
# -----------------------------
df.to_csv(
    "datasets/processed/videos_features.csv",
    index=False
)

print("=" * 60)
print("Feature Engineering Complete")
print("=" * 60)

print()

print(df[["video_id", "combined_text"]].head())

print()

print("Rows :", len(df))
print("Columns :", len(df.columns))