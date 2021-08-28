export PYTHONPATH=.

init:
	pip install -r requirements.txt

test-all:
	py.test tests

test-grep:
	py.test tests -k $(GREP)

pq:
	pip install --editable .

.PHONY: init test