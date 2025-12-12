#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 16:33:23 2025

@author: jordanshaps
"""

import os
import pandas as pd

def test_data(in_folder, out_folder, max_per_genre=50):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    allowed_language = "fr"
    allowed_genres = ["Indie", "Folk", "Pop", "Metal", "Rock"]

    for fname in os.listdir(in_folder):
        if not fname.endswith(".csv"):
            continue

        csv_fpath = os.path.join(in_folder, fname)
        df = pd.read_csv(csv_fpath)
        
        

        # Skip rows whose lyrics contain certain tokens
        df = df[
            ~df["Lyrics"].str.contains("Instrumental", case=False, na=False) &
            ~df["Lyrics"].str.contains("–", na=False) &
            ~df["Lyrics"].str.contains(":", na=False) &
            ~df["Lyrics"].str.contains("Lyrics", case=False, na=False) 
        ]
        
        # Remove empty lines
        df = df[df["Lyrics"].notna()]
        df = df[df["Lyrics"].str.strip() != ""] 

        # Filter by allowed language and genres
        df = df[
            (df["Language"] == allowed_language) &
            (df["Genre"].isin(allowed_genres))
        ]

        limited = (
            df.groupby("Genre", group_keys=False)
              .apply(lambda x: x.head(max_per_genre))
        )

        print(f"\nFile: {fname} — Final Genre Counts:")
        print(limited["Genre"].value_counts())

        if limited.empty:
            print("No valid songs")
            continue

        # Truncate lyrics to be half length
        texts = limited["Lyrics"].apply(
            lambda x: " ".join(str(x).split()[:len(str(x).split()) // 2])
        )

        genres = limited["Genre"].tolist()


        perplex_df = pd.DataFrame({
            "pairid": [1] * len(limited),
            "sentid": list(range(1, len(limited) + 1)),
            "comparison": ["expected"] * len(limited),
            "sentence": texts,
            "source": [allowed_language] * len(limited)
        })

        class_df = pd.DataFrame({
            "textid": list(range(1, len(limited) + 1)),
            "text": texts,
            "target": genres
        })

        perplex_path = os.path.join(out_folder, "perplex_test.tsv")
        class_path = os.path.join(out_folder, "class_test.tsv")

        perplex_df.to_csv(perplex_path, sep="\t", index=False)
        class_df.to_csv(class_path, sep="\t", index=False)

        print(f"Saved: {perplex_path}")
        print(f"Saved: {class_path}")


in_folder = "./raw_data/"
out_folder = "./test_data"
test_data(in_folder, out_folder)