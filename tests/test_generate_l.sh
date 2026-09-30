#!/usr/bin/env bash
set -euo pipefail

root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
bin="$root/results/generate_l_test.exe"
work=$(mktemp -d "$root/results/l_test.XXXXXX")
cleanup() { rm -rf -- "$work" "$bin"; }
trap cleanup EXIT

g++ -std=c++17 -O2 -Wall -Wextra -pedantic \
    "$root/src/entites_nommees/generate_l.cpp" -o "$bin"

input="$work/mini.txt"
out1="$work/liste_L_1.txt"
out2="$work/liste_L_2.txt"
stats="$work/stats.txt"

printf "Hari Seldon visite Éole.\nL'Empire observe Jean-Luc.\nAlpha   Beta, Gamma!\nPont\nNeuf\fSeldon Trantor\n" > "$input"

"$bin" "$out1" "$stats" "$input" >/dev/null
"$bin" "$out2" "$work/stats2.txt" "$input" >/dev/null

count=0
check_contains() {
    local pattern=$1
    local label=$2
    grep -Fqx "$pattern" "$out1" || { echo "ÉCHEC : $label" >&2; exit 1; }
    count=$((count+1))
    printf 'OK %s\n' "$label"
}
check_absent() {
    local pattern=$1
    local label=$2
    if grep -Fqx "$pattern" "$out1"; then
        echo "ÉCHEC : $label" >&2
        exit 1
    fi
    count=$((count+1))
    printf 'OK %s\n' "$label"
}

check_contains $'1\tHari\t1' candidat_simple
check_contains $'1\tÉole\t1' accents_utf8
check_contains $'1\tL\'Empire\t1' apostrophe
check_contains $'1\tJean-Luc\t1' tiret_interne
check_contains $'2\tPont Neuf\t1' retour_ligne_normal
check_contains $'2\tAlpha Beta\t1' espaces_multiples
check_contains $'2\tBeta Gamma\t1' ponctuation
check_contains $'2\tHari Seldon\t1' bigramme_meme_page
check_contains $'3\tHari Seldon visite\t1' trigramme_meme_page
check_absent $'2\tNeuf Seldon\t1' frontiere_u000c
check_absent $'2\tHari Trantor\t1' faux_nom_interpage
check_contains $'1\tGamma\t1' conservation_casse
cmp -s "$out1" "$out2" || { echo "ÉCHEC : determinisme" >&2; exit 1; }
count=$((count+1)); printf 'OK determinisme\n'
python - "$out1" <<'PY'
from pathlib import Path
import sys
Path(sys.argv[1]).read_text(encoding="utf-8")
PY
count=$((count+1)); printf 'OK utf8_valide\n'

grep -Fqx 'traversees_u000c=0' "$stats" || { echo "ÉCHEC : invariant_frontiere" >&2; exit 1; }
count=$((count+1)); printf 'OK invariant_frontiere\n'

printf '%s tests réussis\n' "$count"
