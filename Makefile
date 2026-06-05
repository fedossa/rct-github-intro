all: output/paper.pdf output/presentation.pdf

data/pulled/raw_data.pkl: code/python/pull_data.py
	mkdir -p data/pulled
	uv run python code/python/pull_data.py

data/generated/prepared_data.pkl: code/python/prep_data.py data/pulled/raw_data.pkl
	mkdir -p data/generated
	uv run python code/python/prep_data.py

output/results.pkl: code/python/run_analysis.py data/generated/prepared_data.pkl
	mkdir -p output
	uv run python code/python/run_analysis.py

output/paper.pdf: doc/paper.qmd output/results.pkl
	cd doc && uv run quarto render paper.qmd --to pdf --output paper.pdf
	rm -f doc/paper.tex doc/paper.log doc/paper.aux doc/paper.out doc/paper.knit.md
	rm -f doc/paper.fff doc/paper.ttt doc/texput.log

output/presentation.pdf: doc/presentation.qmd output/results.pkl
	cd doc && uv run quarto render presentation.qmd --output presentation.pdf
	rm -f doc/presentation.tex doc/presentation.log doc/presentation.aux doc/presentation.out doc/presentation.knit.md
	rm -rf output/presentation_files

clean:
	rm -rf data/pulled data/generated output .quarto doc/.quarto
	rm -f doc/*.tex doc/*.log doc/*.aux doc/*.out doc/*.knit.md
