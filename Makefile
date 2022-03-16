python_version := 3.10
SHELL := /bin/bash
VENV := .venv

hello:
	echo "Hello World!"

init:
	python${python_version} -m venv ${VENV}
	${VENV}/bin/python3.10 -m pip install --upgrade pip
	${VENV}/bin/python3.10 -m pip install -r requiremets.txt

freeze:
	${VENV}/bin/python3.10 -m pip freeze > requiremets.txt

clean-freeze:
	rm -rf requiremets.txt

update-freeze: clean-freeze freeze

clean:
	rm -rf ${VENV}
