#!/usr/bin/env bash
set -euo pipefail

printf '%s\n' "=== Zero Authority Witness — Verification Script ==="
printf '%s\n' "Protocol: PRISM"
printf '\n'

printf '%s\n' "1. Running python3 -m unittest discover -s tests -v ..."
python3 -m unittest discover -s tests -v
printf '\n'

printf '%s\n' "2. Running original compat command: python3 zaw.py samples/injected_page.html --task ..."
python3 zaw.py samples/injected_page.html --task "Summarize the refund policy"
printf '\n'

printf '%s\n' "3. Running package CLI: python3 -m zaw.cli witness samples/injected_page.html --task ..."
python3 -m zaw.cli witness samples/injected_page.html --task "Summarize the refund policy"
printf '\n'

printf '%s\n' "4. Verifying pyproject metadata and CLI entry point declaration ..."
python3 - <<'PY'
from pathlib import Path
import tomllib

project = tomllib.loads(Path('pyproject.toml').read_text())
assert project['project']['name'] == 'zero-authority-witness'
assert project['project']['version'] == '0.1.0-rc1'
authors = project['project'].get('authors', [])
assert authors and authors[0].get('email') == 'coresynth@gmail.com'
assert project['project']['scripts']['zaw'] == 'zaw.cli:main'
assert project['project'].get('license', {}).get('file') == 'LICENSE'
print('pyproject metadata OK')
PY
python3 -m zaw.cli version
printf '\n'

printf '%s\n' "5. Confirming check-action on hostile sample: BLOCK expected."
LATEST_RUN="$(ls -1 runs/ | grep '^zaw-' | sort | tail -1)"
EVIDENCE_PATH="runs/${LATEST_RUN}/evidence_packet.json"
set +e
CHECK_OUTPUT="$(python3 -m zaw.cli check-action samples/proposed_action_bad.json --greenlight samples/greenlight.json --evidence "${EVIDENCE_PATH}" 2>&1)"
CHECK_STATUS=$?
set -e
printf '%s\n' "${CHECK_OUTPUT}"
if ! printf '%s\n' "${CHECK_OUTPUT}" | grep -q "Action check verdict: BLOCK"; then
  printf '%s\n' "ERROR: check-action did not return BLOCK." >&2
  exit 1
fi
if [ "${CHECK_STATUS}" -eq 0 ]; then
  printf '%s\n' "ERROR: check-action returned exit code 0 for a BLOCK verdict." >&2
  exit 1
fi
printf '%s\n' "check-action returned BLOCK with non-zero exit as expected."
printf '\n'

printf '%s\n' "=== Verification script finished ==="
printf '%s\n' "PASS_WITH_NOTES: tests, witness demos, metadata check, CLI version, and hostile action BLOCK check all completed."
