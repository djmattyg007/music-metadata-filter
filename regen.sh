#!/bin/bash

set -euo pipefail

UPSTREAM_VERSION="079172b927237f98a570169762f2d005e8015fb2"

cd "$(dirname "$(readlink -f "$0")")"

git clone https://github.com/web-scrobbler/metadata-filter.git upstream

pushd upstream
git checkout "${UPSTREAM_VERSION}"
popd

python3 scripts/rules_gen.py "upstream/src/rules.ts" > "music_metadata_filter/rules.py"

rm -rf "tests/fixtures/filters"
cp -r "upstream/test/fixtures/filters" "tests/fixtures/filters"
python3 scripts/format_test_fixtures.py "tests/fixtures/filters"

rm -rf "tests/fixtures/functions"
cp -r "upstream/test/fixtures/functions" "tests/fixtures/functions"
# We don't need to test this because we use the python stdlib for this functionality
rm "tests/fixtures/functions/decode-html-entities.json"
python3 scripts/format_test_fixtures.py "tests/fixtures/functions"

rm -rf upstream
