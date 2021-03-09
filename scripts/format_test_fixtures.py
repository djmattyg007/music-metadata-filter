import json
import os
import sys


try:
    path = sys.argv[1]
except IndexError:
    sys.stderr.write("Path to test fixtures not supplied.\n")
    sys.exit(1)


with os.scandir(path) as it:
    for entry in it:
        if entry.name.endswith(".json"):
            with open(entry.path, mode="r", encoding="utf-8") as fixture_in:
                fixture = json.load(fixture_in)
            with open(entry.path, mode="w", encoding="utf-8") as fixture_out:
                json.dump(fixture, fixture_out, indent=4)
                fixture_out.write("\n")
