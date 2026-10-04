#!/bin/sh
set -e

cd $(dirname $0)

export DJANGO_SETTINGS_MODULE="core.settings"

# Add a root dir for correct imports
export PYTHONPATH=..

# warm-up
python -m warmup

# Test 1 -> Single-row retrieval as a model instance
python -m test_1

# Test 2 -> Single-row retrieval as a key-value dictionary
python -m test_2

# Test 3 -> Single-row retrieval as a tuple of field values
python -m test_3

# Test 4 -> Retrieval of 1,000 rows as model instances
python -m test_4

# Test 5 -> Retrieval of 1,000 rows as key-value dictionaries
python -m test_5

# Test 6 -> Retrieval of 1,000 rows as tuples of field values
python -m test_6
