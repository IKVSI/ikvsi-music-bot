SHELL := /bin/bash
VENV := .venv
python_version := 3.10
python := ${VENV}/bin/python${python_version}
pip := ${python} -m pip
black := ${python} -m black
yamlfix := ${VENV}/bin/yamlfix

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

format-black:
	${black} src/*

check-black:
	${black} --check src/*

format-yamlfix:
	find ./ -type f -regextype posix-extended -regex ".*\.yml$$" | xargs ${yamlfix}


format: format-black format-yamlfix

check: check-black format-yamlfix
	git diff
