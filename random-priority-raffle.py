#!/usr/bin/env python3

import os
import sys
import random
from pprint import pprint

import yaml

import raffle

# ------------------------
#  Command-line interface
# ------------------------

USAGE = f"""
Usage: {os.path.basename(__file__)} config_file [random_seed]

    config_file (required):
        Raffle configuration file in YAML format. See config.sample.yaml
        for an example.
    random_seed (optional):
        An optional seed value to use for the underlying random number
        generator. Use this parameter for greater control and repeatable
        results. If not specified, the random number generator will use
        cryptographic random values provided by the operating system.

"""

try:
    with open(sys.argv[1], 'r') as config_file:
        configuration = yaml.safe_load(config_file)

    random_seed = sys.argv[2] if len(sys.argv) > 2 else None

except (IndexError, IOError, yaml.parser.ParserError) as e:
    sys.stderr.write(USAGE)
    raise e

try:
    prizes = configuration['prizes']
    entries = configuration['entries']
    preferences = configuration['preferences']
except KeyError as e:
    sys.stderr.write(f"Invalid configuration file: {repr(e)}\n")
    sys.exit(1)

if random_seed:
    print(f"Using random seed: {random_seed}")
    random_source = random.Random(random_seed)
else:
    print("Using system random number generator")
    random_source = random.SystemRandom()

print("Running raffle with configuration:")
pprint(configuration)

results = raffle.raffle(prizes, entries, preferences, random_source)
print("=" * 78)
print("Results:\n")
for participant in sorted(results):
    print(f"{participant} -> {results[participant]}")
