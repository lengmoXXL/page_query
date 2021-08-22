init:
	pip install -r requirements.txt

test:
	py.test tests

pq:
	pyinstaller page_query/main.py -n pq	

.PHONY: init test