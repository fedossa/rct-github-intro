# rct-project-template

This repository is the **Python version of a barebones project template**. It is meant to be small enough to understand quickly, but structured enough to grow into a real project.

The main idea is simple:

- data are pulled into `data/pulled/`
- data are prepared into `data/generated/`
- analysis writes a serialized results bundle to `output/`
- the paper in `doc/` reads those saved results

So even though the example uses the tiny `mtcars` dataset, the workflow is already organized like a real empirical project.

## What You Are Looking At

This repository gives you a minimal project skeleton with four visible stages:

1. `code/python/pull_data.py`
2. `code/python/prep_data.py`
3. `code/python/run_analysis.py`
4. `doc/paper.qmd`

The point is not the `mtcars` analysis itself. The point is to give you a clean starting structure that you can keep extending for your own work.

If you later look at `trr266/treat`, you will see the same broad movement in a richer and more elaborate form.

## Project Structure

```text
.devcontainer/
.python-version
README.md
Makefile
pyproject.toml
uv.lock
code/python/pull_data.py
code/python/prep_data.py
code/python/run_analysis.py
data/
  external/
  pulled/
  generated/
  data_readme.md
doc/
  paper.qmd
  references.bib
output/
```

## How The Workflow Moves

The workflow is intentionally explicit:

1. `pull_data.py` creates a raw object in `data/pulled/`
2. `prep_data.py` reads that raw object and creates a prepared analysis dataset in `data/generated/`
3. `run_analysis.py` reads the prepared dataset and writes a serialized `.pkl` results bundle to `output/`
4. `doc/paper.qmd` reads that `.pkl` bundle and renders the paper

The paper does **not** rerun the full analysis pipeline internally. It consumes prepared results from `output/`.

## The `data/` Folder

The `data/` folder keeps the same conceptual separation used in `treat`:

- `data/external/`: files that come from outside the repository and are kept as source material
- `data/pulled/`: raw data written by a pull step
- `data/generated/`: prepared datasets created from raw or external inputs

In this template, the pull step uses the built-in `mtcars` dataset that ships with `plotnine`, so `data/external/` starts empty. The folder is still there so you can swap in your own real project data later without changing the overall structure.

## References

The paper also includes a minimal bibliography workflow. The bibliography file lives at:

- `doc/references.bib`

and `doc/paper.qmd` cites at least one reference from that file. That way you can already see the basic citation pattern in a working template rather than adding it later from scratch.

## Recommended Setup Paths

There are three ways to work with this repo:

1. **GitHub Codespaces**
   This is the recommended path.
2. **Local VS Code + Docker Dev Containers**
   This is the recommended local path.
3. **Fully local install**
   This is possible, but not recommended.

### 1. GitHub Codespaces

1. Use this template on GitHub to create your own repository.
2. Open your repository in Codespaces.
3. Wait for the devcontainer to finish building.
4. Wait for the post-create step to finish running `uv sync`.
5. In the Codespaces terminal, run:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
gh auth login
make
```

The repository-local virtual environment lives at `.venv/`. Codespaces should detect it automatically and use it as the Python interpreter. The interpreter itself is managed by `uv`, which downloads the Python version pinned in `.python-version`.

### 2. Local VS Code + Docker Dev Containers

1. Install Docker.
2. Install VS Code plus the Dev Containers extension.
3. Open the repository in VS Code.
4. Run `Dev Containers: Reopen in Container` from the Command Palette.
5. Wait for the devcontainer build and the post-create `uv sync` step to finish.
6. In the integrated terminal inside the container, run:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
gh auth login
make
```

The devcontainer keeps the project virtual environment in `.venv/` and configures VS Code to use it automatically. `uv` also manages the Python interpreter for that environment, so the container image does not need to ship the project Python version directly.

### 3. Fully Local Install

You can also run the project outside containers, but this is **not recommended** unless you are comfortable managing the stack yourself:

- `uv`
- Quarto
- a LaTeX installation capable of rendering PDFs
- Git and optionally GitHub CLI

If you choose this route, run:

```bash
uv sync --managed-python
source .venv/bin/activate
make
```

## Main Project Command

Run the whole project from the repository root with:

```bash
make
```

The Makefile runs the full pipeline in order:

1. `code/python/pull_data.py`
2. `code/python/prep_data.py`
3. `code/python/run_analysis.py`
4. `doc/paper.qmd`

## Outputs

The main analytical output is:

- `output/rct-project-template-results.pkl`

The final paper is written to:

- `output/rct-project-template-paper.pdf`

That paper imports one saved descriptive table and one saved figure from the results bundle. The analytical objects are prepared first, then rendered in the paper.

## The Paper

The paper source lives in:

- `doc/paper.qmd`

It is formatted as a small article-style paper so the repository already feels like a miniature research template rather than a single script with a report attached at the end.
The current template shows one descriptive table, one figure, and one bibliography entry so the reporting workflow stays visible without becoming crowded.

## Container Notes

Both Codespaces and the local devcontainer path provide:

- `uv`
- `git`
- `gh`
- Quarto
- TinyTeX

In both container paths, `uv` downloads and manages the Python interpreter pinned for the project. This keeps the working environment consistent across students without baking the project Python version into the base image.

To keep the image build lighter, the devcontainer does not preinstall an extra bundle of LaTeX packages. If Quarto reports a missing LaTeX package when rendering `output/rct-project-template-paper.pdf`, install that package on demand with `tlmgr install <package>`.
