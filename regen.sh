#!/bin/bash

set -euo pipefail

UPSTREAM_VERSION="7ff7b4bf27ae12aec399a46994ce43a78a0fe333"

cd "$(dirname -- "$(readlink -f "$0")")"

git clone https://github.com/web-scrobbler/metadata-filter.git upstream

pushd upstream
git checkout "${UPSTREAM_VERSION}"
popd

python3 scripts/rules_gen.py "upstream/src/rules.ts" > "music_metadata_filter/rules.py"

rm -rf "tests/fixtures/functions"
cp -r "upstream/test/fixtures/functions" "tests/fixtures/functions"
# We don't need to test this because we use the python stdlib for this functionality
rm "tests/fixtures/functions/decode-html-entities.json"
python3 scripts/format_test_fixtures.py "tests/fixtures/functions"

rm -rf upstream
