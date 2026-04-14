from pathlib import Path

from plotnine.data import mtcars


OUTPUT_PATH = Path("data/pulled/mtcars_raw.pkl")


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    mtcars_raw = mtcars.copy()
    mtcars_raw.index.name = "model"
    mtcars_raw = mtcars_raw.reset_index()

    mtcars_raw.to_pickle(OUTPUT_PATH)


if __name__ == "__main__":
    main()
