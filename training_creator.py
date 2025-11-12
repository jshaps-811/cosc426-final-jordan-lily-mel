import os
import pandas as pd
import math

def training_creator(in_folder, out_folder, max_per_genre=350, val_ratio=0.1):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    allowed_languages = ["en", "pt"]
    allowed_genres = ["Indie", "Folk", "Pop", "Metal", "Rock"]

    for fname in os.listdir(in_folder):
        if not fname.endswith(".csv"):
            continue

        csv_fpath = os.path.join(in_folder, fname)
        df = pd.read_csv(csv_fpath)

        # Filter by allowed languages and genres
        df = df[df["Language"].isin(allowed_languages) & df["Genre"].isin(allowed_genres)]

        # Limit to max_per_genre songs per language and genre
        limited_df = df.groupby(["Language", "Genre"], group_keys=False).apply(lambda x: x.head(max_per_genre))

        print(f"File: {fname} — Final counts per language & genre:")
        print(limited_df.groupby(["Language", "Genre"]).size())

        for lang in allowed_languages:
            lang_df = limited_df[limited_df["Language"] == lang].copy()
            if lang_df.empty:
                continue

            # Use half of the lyrics for the text
            lang_df["text"] = lang_df["Lyrics"].apply(lambda x: " ".join(str(x).split()[:len(str(x).split()) // 2]))
            lang_df["label"] = lang_df["Genre"]
            lang_df["language"] = lang_df["Language"]

            train_rows = []
            val_rows = []

            # Deterministic split per genre: first N for validation, rest for training
            for genre, group in lang_df.groupby("label"):
                n_val = max(1, math.ceil(len(group) * val_ratio))  # at least 1
                val_rows.append(group.iloc[:n_val])
                train_rows.append(group.iloc[n_val:])

            train_df = pd.concat(train_rows).reset_index(drop=True)
            val_df = pd.concat(val_rows).reset_index(drop=True)

            # Add sequential sentid
            train_df.insert(0, "textid", range(1, len(train_df) + 1))
            val_df.insert(0, "textid", range(1, len(val_df) + 1))

            # Save training data
            train_path = os.path.join(out_folder, f"{lang}_training_data.tsv")
            train_df[["textid", "text", "label"]].to_csv(train_path, sep="\t", index=False)
            print(f"Saved {train_path} — {len(train_df)} rows")

            # Save validation data
            val_path = os.path.join(out_folder, f"{lang}_validation_data.tsv")
            val_df[["textid", "text", "label"]].to_csv(val_path, sep="\t", index=False)
            print(f"Saved {val_path} — {len(val_df)} rows")


# Example usage
in_folder = "./raw_data/"
out_folder = "./norm_data/"
training_creator(in_folder, out_folder)
