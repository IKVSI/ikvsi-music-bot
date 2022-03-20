SHELL := /bin/bash
VENV := .venv
python_version := 3.10
python := ${VENV}/bin/python${python_version}
pip := ${python} -m pip

init:
	python${python_version} -m venv ${VENV}
	${pip} install --upgrade pip
	${pip} install -r requiremets.txt

clean:
	rm -rf ${VENV}

freeze:
	${pip} freeze > requiremets.txt

upgrade-freeze:
	cat requiremets.txt | awk '{split($$0,r,"=="); print(r[1])}' | xargs ${pip} install -U

upgrade: upgrade-freeze freeze


pip-install:
	${pip} install ${packet}

install: pip-install freeze
