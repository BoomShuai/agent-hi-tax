#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(dirname "$script_dir")
cd "$repo_root"

manifests=$(
  find runs -mindepth 3 -maxdepth 3 -type f -name manifest.yaml -print |
    LC_ALL=C sort
)

if [ -z "$manifests" ]; then
  echo "no run packages found" >&2
  exit 1
fi

printf '%s\n' "$manifests" |
  while IFS= read -r manifest; do
    package_dir=${manifest%/manifest.yaml}
    ./scripts/verify-run-package.sh "$package_dir"
  done

python3 scripts/build-results-index.py --check
echo "all run packages and the results index are verified"
