#!/usr/bin/env bash
set -euo pipefail

root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
export LC_ALL=C.utf8

for tool in g++ python; do
    command -v "$tool" >/dev/null || { echo "Outil absent : $tool" >&2; exit 1; }
done

inputs=(
    "$root/results/processed/Fondation.txt"
    "$root/results/processed/Fondation_et_empire.txt"
    "$root/results/processed/Seconde_Fondation.txt"
)
for input in "${inputs[@]}"; do
    [[ -f "$input" && -s "$input" ]] || { echo "Source processed absente/vide : $input" >&2; exit 1; }
    python - "$input" <<'PY'
from pathlib import Path
import sys
Path(sys.argv[1]).read_text(encoding="utf-8")
PY
done

mkdir -p "$root/results/lists"
bin=$(mktemp "$root/results/lists/generate_l.XXXXXX.exe")
cleanup() { rm -f -- "$bin"; }
trap cleanup EXIT

g++ -std=c++17 -O2 -Wall -Wextra -pedantic \
    "$root/src/entites_nommees/generate_l.cpp" -o "$bin"

"$bin" \
    "$root/results/lists/liste_L.txt" \
    "$root/results/lists/liste_L_stats.txt" \
    "${inputs[@]}"

python - "$root/results/lists/liste_L.txt" "$root/results/lists/liste_L_stats.txt" <<'PY'
from pathlib import Path
import sys
for name in sys.argv[1:]:
    Path(name).read_text(encoding="utf-8")
print("Sorties UTF-8 : OK")
PY
