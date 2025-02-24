[![PyPI version](https://badge.fury.io/py/aspa_eval.svg)](https://badge.fury.io/py/aspa_eval)
![PyPy](https://img.shields.io/badge/PyPy-7.3.17-blue)
![Tests](https://github.com/jfuruness/aspa_eval/actions/workflows/tests.yml/badge.svg)
![Linux](https://img.shields.io/badge/os-Linux-blue.svg)
![macOS Intel](https://img.shields.io/badge/os-macOS_Intel-lightgrey.svg)
![macOS ARM](https://img.shields.io/badge/os-macOS_ARM-lightgrey.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-2A6DBA.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint/tree/main)
[![try/except style: tryceratops](https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black)](https://github.com/guilatrova/tryceratops)

# aspa\_eval

Conference slides: https://docs.google.com/presentation/d/1WQXK-JlCqNEaWqtDYI7O-UOUiYpUVPjM0oXznlxZyaY/edit?usp=sharing

If you're looking for the ROV datasets: github.com/jfuruness/rov_collector


* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [License](#license)

## Package Description

See Securing BGP ASAP: ASPA and Other Post-ROV Defenses

If you're looking for the ROV dataset, see github.com/jfuruness/rov_collector

This package runs all simulations and generates graphs for the conference paper above. These simulations are also powered by BGPy (github.com/jfuruness/bgpy_pkg). Check out the tutorial there for more info.

Any questions feel free to email me at jfuruness@gmail.com

## Usage
* [aspa\_eval](#aspa\_eval)

```
pypy3 -O -m aspa_eval --trials=100
```

## Installation
* [aspa\_eval](#aspa\_eval)

Install python and pip if you have not already.

NOTE: You really need PyPy for any speed on this

Then run:

```bash
# Needed for graphviz and Pillow
# Download and install pypy from online
pypy3 -m venv pypy_env
source pypy_env/bin/activate
pip3 install pip --upgrade
git clone https://github.com/jfuruness/aspa_eval.git
cd aspa_eval
pip3 install -e .[test]
pre-commit install
```

To test the development package: [Testing](#testing)


## Testing
* [aspa\_eval](#aspa\_eval)

To test the package after installation, you're going to need the normal python environment rather than using pypy:

```
deactivate
python3 -m venv env
source env/bin.activate
cd aspa_eval
pytest aspa_eval
ruff check aspa_eval
ruff format aspa_eval
mypy aspa_eval
```

Alternatively you can run this using tox:

```
cd aspa_eval
tox --skip-missing-interpreters
```


## Development/Contributing
* [aspa\_eval](#aspa\_eval)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Test it
5. Run tox
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin my-new-feature`
8. Ensure github actions are passing tests
9. Email me at jfuruness@gmail.com if it's been a while and I haven't seen it

## License
* [aspa\_eval](#aspa\_eval)

BSD License (see license file)
