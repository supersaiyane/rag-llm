lint:
	ruff check .

format:
	ruff check . --fix
	black .

format-check:
	black --check .


#make lint
#make format