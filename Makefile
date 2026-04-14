UV := uv
UV_SYNC := $(UV) sync --managed-python --locked
PYTHON := .venv/bin/python
QUARTO := quarto
QUARTO_PYTHON := $(abspath $(PYTHON))

PULLED := data/pulled/mtcars_raw.pkl
GENERATED := data/generated/mtcars_prepared.pkl
RESULTS := output/rct-project-template-results.pkl
FIGURE := output/rct-project-template-scatter-figure.png
PAPER_BASENAME := rct-project-template-paper.pdf
PAPER := output/$(PAPER_BASENAME)
SOURCE := doc/paper.qmd

.PHONY: all clean

all: $(PAPER)

$(PYTHON): pyproject.toml uv.lock .python-version
	$(UV_SYNC)

$(PULLED): code/python/pull_data.py $(PYTHON)
	mkdir -p data/pulled
	$(PYTHON) $<

$(GENERATED): code/python/prep_data.py $(PULLED) $(PYTHON)
	mkdir -p data/generated
	$(PYTHON) $<

$(RESULTS): code/python/run_analysis.py $(GENERATED) $(PYTHON)
	mkdir -p output
	$(PYTHON) $<

$(PAPER): $(SOURCE) $(RESULTS) $(PYTHON)
	rm -rf .quarto doc/.quarto
	cd doc && QUARTO_PYTHON=$(QUARTO_PYTHON) $(QUARTO) render paper.qmd --to pdf --output $(PAPER_BASENAME)
	rm -f paper.tex paper.log paper.aux paper.out paper.knit.md
	rm -f $(PAPER_BASENAME)
	rm -f texput.log doc/texput.log
	rm -f doc/paper.tex doc/paper.log doc/paper.aux doc/paper.out doc/paper.knit.md doc/paper.fff doc/paper.ttt

clean:
	rm -rf .quarto doc/.quarto
	rm -f $(PULLED) $(GENERATED) $(RESULTS) $(FIGURE) $(PAPER)
	rm -f paper.tex paper.log paper.aux paper.out paper.knit.md
	rm -f texput.log doc/texput.log
	rm -f doc/paper.tex doc/paper.log doc/paper.aux doc/paper.out doc/paper.knit.md doc/paper.fff doc/paper.ttt
