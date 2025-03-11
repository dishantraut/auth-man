PYTHON := python3
REQS := requirements.txt

.PHONY: all venv install clean

venv:
	$(PYTHON) -m venv venv

install:
	which pip python3
	python3 -m pip install -U pip wheel setuptools
	pip install --no-cache-dir -r $(REQS)

clean-venv:
	rm -rf $(VENV)

# start:
# 	docker start $(docker ps -aq --filter name=authman)

# stop:
# 	docker stop $(docker ps -aq --filter name=authman)