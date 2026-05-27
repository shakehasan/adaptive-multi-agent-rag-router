PYTHON ?= python
PYTHONPATH := src

.PHONY: install test lint demo ingest ask evaluate traces count-lines check-names clean serve benchmark-routing

install:
	$(PYTHON) -m pip install -e .

test:
	PYTHONPATH=$(PYTHONPATH) PYTHONDONTWRITEBYTECODE=1 $(PYTHON) scripts/run_all_tests.py

lint:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/syntax_check.py

demo:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m amarr.cli.main serve --mock --port 8765

serve:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m amarr.cli.main serve --mock --port 8765

ingest:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m amarr.cli.main ingest examples/documents

ask:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m amarr.cli.main ask "What principles guide reliable local AI systems?"

evaluate:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m amarr.cli.main evaluate

traces:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m amarr.cli.main trace latest

benchmark-routing:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m amarr.cli.main benchmark-routing

count-lines:
	$(PYTHON) scripts/count_lines.py

check-names:
	$(PYTHON) scripts/check_forbidden_names.py

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(p, ignore_errors=True) for p in map(Path, ['.amarr','build','dist','htmlcov'])]"
