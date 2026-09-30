#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
export LC_ALL=C.utf8
mkdir -p "$root/results/processed"
actual=$(mktemp "$root/results/processed/.test.XXXXXX")
expected=$(mktemp "$root/results/processed/.expected.XXXXXX")
trap 'rm -f -- "$actual" "$expected"' EXIT
count=0
check() {
    printf '%s' "$2" > "$expected"
    printf '%s' "$1" | gawk -f "$root/scripts/preprocess.awk" > "$actual" 2>/dev/null
    cmp -s "$expected" "$actual" || { echo "ÉCHEC : $3" >&2; exit 1; }
    count=$((count+1))
    printf 'OK %s\n' "$3"
}
check $'Hari Seldon regardait par\nla fenêtre.' 'Hari Seldon regardait par la fenêtre.' continuation
check $'vous-\nmême' 'vous-même' tiret
check $'fin page\fdébut page suivante' $'fin page\fdébut page suivante' frontiere
check '± 17 ±' '' pagination
check 'La valeur ± quelque chose' 'La valeur ± quelque chose' symbole_narratif
check '- Bonjour.' '- Bonjour.' dialogue
check 'Hari Seldon était à Terminus.' 'Hari Seldon était à Terminus.' casse
check 'é è ê à ù ç œ Œ' 'é è ê à ù ç œ Œ' accents
check $'Le silence\nune voix' $'Le silence\nune voix' ambigu
check $'vous-\fmême' $'vous-\fmême' tiret_frontiere
check $'Hari Seldon regardait par\fla fenêtre.' $'Hari Seldon regardait par\fla fenêtre.' continuation_frontiere
check $'± 17 ±\ntexte narratif' $'± 17 ±\ntexte narratif' nombre_interne
check $'Texte\n- 5 -\fSuite' $'Texte\fSuite' pied_frontiere
check $'CHAPITRE\nla suite' $'CHAPITRE\nla suite' titre
check $'Hari Seldon regardait par\n\nla fenêtre.' $'Hari Seldon regardait par\n\nla fenêtre.' paragraphe
check $'- Hari Seldon regardait par\nla fenêtre.' $'- Hari Seldon regardait par\nla fenêtre.' dialogue_continu
check $'frag-\nment' $'frag-\nment' tiret_inconnu
check "l'homme ° ¶ (cid:10) ±" "l'homme ° ¶ (cid:10) ±" artefacts
printf '%s tests réussis\n' "$count"
