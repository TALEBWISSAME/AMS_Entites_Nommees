#!/usr/bin/env bash
set -euo pipefail

root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
work=$(mktemp -d "$root/results/lp_test.XXXXXX")
cleanup() { rm -rf -- "$work"; }
trap cleanup EXIT

input="$work/liste_L_artificielle.txt"
out1="$work/liste_LP_1.txt"
out2="$work/liste_LP_2.txt"
stats1="$work/stats_1.txt"
stats2="$work/stats_2.txt"

cat > "$input" <<'DATA'
n	forme	frequence
1	Seldon	12
2	Hari Seldon	7
1	Alors	30
1	Élodie	3
1	L'Empereur	2
1	Jean-Luc	4
1	Bayta	9
1	HARI	2
1	Maire	5
1	Trantor	8
2	Hari marche	2
2	Monsieur Dupont	2
1	Pierre	1
1	Cité	1
DATA

hash_before=$(python - "$input" <<'PY'
from hashlib import sha256
from pathlib import Path
import sys
print(sha256(Path(sys.argv[1]).read_bytes()).hexdigest())
PY
)

python "$root/scripts/generate_lp.py" --input "$input" --output "$out1" --stats "$stats1" >/dev/null
python "$root/scripts/generate_lp.py" --input "$input" --output "$out2" --stats "$stats2" >/dev/null

hash_after=$(python - "$input" <<'PY'
from hashlib import sha256
from pathlib import Path
import sys
print(sha256(Path(sys.argv[1]).read_bytes()).hexdigest())
PY
)

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

check_contains $'Seldon\t12\t1\tunigramme_majuscule_frequent' nom_simple
check_contains $'Hari Seldon\t7\t2\t2gramme_nominal_majuscule' nom_compose
check_absent $'Alors\t30\t1\tunigramme_majuscule_frequent' debut_phrase_rejete
check_contains $'Élodie\t3\t1\tunigramme_majuscule_frequent' accents_utf8
check_contains $'L\'Empereur\t2\t1\tunigramme_majuscule_frequent' apostrophe
check_contains $'Jean-Luc\t4\t1\tunigramme_majuscule_frequent' tiret_interne
check_contains $'Bayta\t9\t1\tunigramme_majuscule_frequent' frequence_conservee
cmp -s "$out1" "$out2" || { echo "ÉCHEC : determinisme" >&2; exit 1; }
count=$((count+1)); printf 'OK determinisme\n'
[[ "$hash_before" == "$hash_after" ]] || { echo "ÉCHEC : fichier_l_modifie" >&2; exit 1; }
count=$((count+1)); printf 'OK fichier_l_original_non_modifie\n'
grep -Fqx 'ambigus=3' "$stats1" || { echo "ÉCHEC : cas_ambigu" >&2; exit 1; }
count=$((count+1)); printf 'OK cas_ambigu\n'
check_contains $'HARI\t2\t1\tunigramme_majuscule_frequent' variante_casse
if [[ -e "$work/liste_LL.txt" ]]; then echo "ÉCHEC : absence_ll" >&2; exit 1; fi
count=$((count+1)); printf 'OK absence_ll\n'
check_absent $'Hari marche\t2\t2\t2gramme_nominal_majuscule' absence_faux_ngramme_contextuel
python - "$out1" "$stats1" <<'PY'
from pathlib import Path
import sys
for name in sys.argv[1:]:
    Path(name).read_text(encoding="utf-8")
PY
count=$((count+1)); printf 'OK utf8_valide\n'
grep -Fqx 'artefacts_rejetes=0' "$stats1" || { echo "ÉCHEC : stats_artefacts" >&2; exit 1; }
count=$((count+1)); printf 'OK stats_artefacts\n'

printf '%s tests réussis\n' "$count"
