# Canonical challenge report

## Motivation

Retrieve the 10 most popular package in the debian release.

I spent ~ 4 hours understanding the assignment, writing the code, unittests and
validate coding styled

Step I took to complete the assignement:

- First undertand the Content file
- Plan a script to extract the desired data
- Writing the script:
  - parse the arg to get the architecture from the runtime parameter
  - download the content file
  - unzip the file
  - read line by line the extracted file
  - apply the string manipulation to extract the packages on the line
  - store number of appearance in a dictionary
  - output the 10 first most present packages

## Installation
I used poetry to install my depedencies

```bash
poetry install
```
you can also only use pip

```bash
pip install requests pytest prospector isort
```

## Running the script
To retrieve the 10 most popular package for arm64 using poetry
```bash
poetry run package_statistic.py arm64
```
Or
```bash
chmod +x package_statistic.py
./package_statistic.py arm64
```

## Running the tests
```bash
poetry run pytest package_statistic_test.py
```
Or
```bash
pytest package_statistic_test.py
```

## Linting the code
I use the tool called `prospector` and `isort`
```bash
prospector --strictness high
isort package_statistic.py package_statistic_test.py
```
