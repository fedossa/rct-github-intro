from pathlib import Path
import pickle

import pandas as pd
import statsmodels.formula.api as smf
from plotnine import (
    aes,
    element_blank,
    geom_point,
    geom_smooth,
    ggplot,
    labs,
    scale_color_manual,
    theme,
    theme_minimal,
)


INPUT_PATH = Path("data/generated/mtcars_prepared.pkl")
RESULTS_PATH = Path("output/rct-project-template-results.pkl")
FIGURE_PATH = Path("output/rct-project-template-scatter-figure.png")


def prepare_descriptive_table(data: pd.DataFrame) -> pd.DataFrame:
    summary = (
        data.groupby("transmission", observed=False)
        .agg(
            n_cars=("model", "size"),
            mpg=("mpg", "mean"),
            hp=("hp", "mean"),
            wt=("wt", "mean"),
        )
        .reset_index()
    )
    summary = summary.sort_values("transmission").reset_index(drop=True)

    summary[["mpg", "hp", "wt"]] = summary[["mpg", "hp", "wt"]].round(1)
    summary["transmission"] = summary["transmission"].astype(str)

    return summary.rename(
        columns={
            "transmission": "Transmission",
            "n_cars": "Cars",
            "mpg": "Mean fuel efficiency (mpg)",
            "hp": "Mean horsepower",
            "wt": "Mean weight (1,000 lbs)",
        }
    )


def make_scatter_figure(data: pd.DataFrame):
    return (
        ggplot(data, aes(x="wt", y="mpg", color="transmission"))
        + geom_point(size=2.6)
        + geom_smooth(method="lm", se=False, size=0.8, fullrange=True)
        + scale_color_manual(values={"Automatic": "#1b6ca8", "Manual": "#d95f02"})
        + labs(
            x="Vehicle weight (1,000 lbs)",
            y="Fuel efficiency (miles per gallon)",
            color="Transmission",
        )
        + theme_minimal(base_size=11)
        + theme(
            legend_position="top",
            panel_grid_minor=element_blank(),
        )
    )


def main() -> None:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    analysis_data = pd.read_pickle(INPUT_PATH)

    model = smf.ols("mpg ~ wt + C(transmission)", data=analysis_data).fit()
    descriptive_table = prepare_descriptive_table(analysis_data)
    scatter_figure = make_scatter_figure(analysis_data)
    scatter_figure.save(FIGURE_PATH, width=6.5, height=4.3, dpi=300, verbose=False)

    highlights = {
        "sample_size": int(len(analysis_data)),
        "avg_mpg": round(float(analysis_data["mpg"].mean()), 1),
        "avg_weight": round(float(analysis_data["wt"].mean()), 2),
        "avg_horsepower": round(float(analysis_data["hp"].mean()), 1),
        "weight_slope": round(float(model.params["wt"]), 2),
        "manual_effect": round(float(model.params["C(transmission)[T.Manual]"]), 2),
        "fastest_model": str(analysis_data.loc[analysis_data["mpg"].idxmax(), "model"]),
        "heaviest_model": str(analysis_data.loc[analysis_data["wt"].idxmax(), "model"]),
        "interpretation": (
            "The prepared sample suggests a clear negative relationship between "
            "vehicle weight and fuel efficiency, while the manual cars in this "
            "small dataset have somewhat higher fuel efficiency after controlling "
            "for weight."
        ),
    }

    results = {
        "descriptive_table": descriptive_table,
        "scatter_figure_path": str(FIGURE_PATH),
        "table_note": (
            "This table summarizes the prepared mtcars sample by transmission type. "
            "Fuel efficiency is measured in miles per gallon and weight is measured "
            "in 1,000 pounds."
        ),
        "highlights": highlights,
    }

    with RESULTS_PATH.open("wb") as results_file:
        pickle.dump(results, results_file)


if __name__ == "__main__":
    main()
