.PHONY: all clean

all: | venv
	venv/bin/python -m poolcal

clean:
	rm -rf venv

venv: requirements.txt
	python -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
