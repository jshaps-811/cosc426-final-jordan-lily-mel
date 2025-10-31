import os
import pandas as pd

def en_lyric(in_folder, out_folder):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    for fname in os.listdir(in_folder):
        if fname.endswith(".csv"):
            csv_fpath = os.path.join(in_folder, fname)

            df = pd.read_csv(csv_fpath)

            lyric_col = []
            genre_col = []
            lang_col  = []

            # track language counts
            lang_counts = {}

            # iterate through rows
            for _, row in df.iterrows():
                lang = row["Language"]
                text = row["Lyrics"]
                genre = row["Genre"]

                # only track these languages
                if lang not in ["en"]:
                    continue

                if lang not in lang_counts:
                    lang_counts[lang] = 0
                if lang_counts[lang] >= 9900:  
                    continue

                lang_col.append(lang)
                lyric_col.append(text)
                genre_col.append(genre)

                lang_counts[lang] += 1

            print(f"File: {fname} — Final Lang Counts:", lang_counts)


            df_out = pd.DataFrame({
                "textid": list(range(len(lang_col))),
                "Language": lang_col,
                "text": lyric_col,
                "target": genre_col
            })

            # shuffle ordering
            df_out = df_out.sample(frac=1, random_state=42).reset_index(drop=True)

            train_rows = []
            valid_rows = []

            for lang in ["en"]:
                lang_data = df_out[df_out["Language"] == lang]

                train_rows.append(lang_data.head(9000))
                valid_rows.append(lang_data.iloc[9000:9900])

            train_df = pd.concat(train_rows).reset_index(drop=True)
            valid_df = pd.concat(valid_rows).reset_index(drop=True)

            # write .tsv files
            train_path = os.path.join(out_folder, "en_train_filtered.tsv")
            valid_path = os.path.join(out_folder, "en_validate_filtered.tsv")

            train_df.to_csv(train_path, sep="\t", index=False)
            valid_df.to_csv(valid_path, sep="\t", index=False)

            print(f"Saved TRAIN → {train_path} ({len(train_df)})")
            print(f"Saved VALIDATE → {valid_path} ({len(valid_df)})")


in_folder = "./raw_data/"
out_folder = "./norm_data/"

en_lyric(in_folder, out_folder)
