from helpers import COUNTIES, YEARS

import pandas as pd


def generate_file_names() -> list[str]:
    file_names = []
    for year in YEARS:
        for name, id in COUNTIES.items():
            file_names.append(f"data/{year}/{name}.csv")
    return file_names


def combine_files():
    return pd.concat((pd.read_csv(f) for f in generate_file_names()))


def export_single_file():
    df = combine_files()
    df.to_csv("data/composite.csv", index=False)


export_single_file()