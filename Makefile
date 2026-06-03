UV := uv
PYTHON := .venv/bin/python
QUARTO_PYTHON := $(abspath $(PYTHON))

all: output/paper.pdf output/presentation.pdf

$(PYTHON): pyproject.toml uv.lock .python-version
	$(UV) sync --managed-python --locked

data/pulled/raw_data.pkl: code/python/pull_data.py $(PYTHON)
	mkdir -p data/pulled
	$(PYTHON) code/python/pull_data.py

data/generated/prepared_data.pkl: code/python/prep_data.py data/pulled/raw_data.pkl $(PYTHON)
	mkdir -p data/generated
	$(PYTHON) code/python/prep_data.py

output/results.pkl: code/python/run_analysis.py data/generated/prepared_data.pkl $(PYTHON)
	mkdir -p output
	$(PYTHON) code/python/run_analysis.py

output/paper.pdf: doc/paper.qmd output/results.pkl $(PYTHON)
	cd doc && QUARTO_PYTHON=$(QUARTO_PYTHON) quarto render paper.qmd --to pdf --output paper.pdf
	rm -f doc/paper.tex doc/paper.log doc/paper.aux doc/paper.out doc/paper.knit.md
	rm -f doc/paper.fff doc/paper.ttt doc/texput.log

output/presentation.pdf: doc/presentation.qmd output/results.pkl $(PYTHON)
	cd doc && QUARTO_PYTHON=$(QUARTO_PYTHON) quarto render presentation.qmd --output presentation.pdf
	rm -f doc/presentation.tex doc/presentation.log doc/presentation.aux doc/presentation.out doc/presentation.knit.md
	rm -rf output/presentation_files

clean:
	rm -rf data/pulled data/generated output .quarto doc/.quarto
	rm -f doc/*.tex doc/*.log doc/*.aux doc/*.out doc/*.knit.md
