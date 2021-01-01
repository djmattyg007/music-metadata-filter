#!/bin/bash

set -e

UPSTREAM_VERSION="eba9846aeaebebe52d9b0f337555eede37314824"

cd "$(dirname -- "$(readlink -f "$0")")"

git clone https://github.com/djmattyg007/metadata-filter.git upstream

pushd upstream
git checkout "${UPSTREAM_VERSION}"
popd

python3 scripts/rules_gen.py upstream/src/rules.ts > music_metadata_filter/rules.py

rm -rf "tests/fixtures/function"
cp -r "upstream/test/fixtures/function" "tests/fixtures/function"
# We don't need to test this because we use the python stdlib for this functionality
rm "tests/fixtures/function/decode-html-entities.json"

rm -rf upstream
