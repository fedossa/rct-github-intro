from pathlib import Path

import numpy as np
import pandas as pd


INPUT_PATH = Path("data/pulled/mtcars_raw.pkl")
OUTPUT_PATH = Path("data/generated/mtcars_prepared.pkl")


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    raw_data = pd.read_pickle(INPUT_PATH)

    prepared_data = raw_data.assign(
        transmission=pd.Categorical(
            np.where(raw_data["am"] == 1, "Manual", "Automatic"),
            categories=["Automatic", "Manual"],
            ordered=True,
        ),
        cylinders=pd.Categorical(raw_data["cyl"], categories=[4, 6, 8], ordered=True),
        weight_kg=(raw_data["wt"] * 453.592).round(0).astype(int),
        efficiency_band=np.where(
            raw_data["mpg"] >= raw_data["mpg"].median(),
            "Higher mpg",
            "Lower mpg",
        ),
    )[
        [
            "model",
            "mpg",
            "hp",
            "wt",
            "weight_kg",
            "cylinders",
            "transmission",
            "efficiency_band",
            "disp",
            "qsec",
        ]
    ]

    prepared_data.to_pickle(OUTPUT_PATH)


if __name__ == "__main__":
    main()
