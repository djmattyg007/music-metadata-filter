#!/bin/bash

set -e

UPSTREAM_VERSION="c8ecc5501bb0f6f7bdfd3af09e394fe89c80bf9d"

cd "$(dirname -- "$(readlink -f "$0")")"

git clone https://github.com/web-scrobbler/metadata-filter.git upstream

pushd upstream
git checkout "${UPSTREAM_VERSION}"
popd

python3 scripts/rules_gen.py upstream/src/rules.ts > music_metadata_filter/rules.py

rm -rf "tests/fixtures/functions"
cp -r "upstream/test/fixtures/functions" "tests/fixtures/functions"
# We don't need to test this because we use the python stdlib for this functionality
rm "tests/fixtures/functions/decode-html-entities.json"

rm -rf upstream
