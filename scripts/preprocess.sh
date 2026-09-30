#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
export LC_ALL=C.utf8
for tool in gawk iconv sha256sum mktemp cmp; do
    command -v "$tool" >/dev/null || { echo "Outil absent : $tool" >&2; exit 1; }
done
# Vérifie réellement le traitement multioctet plutôt que supposer la locale.
gawk 'BEGIN {exit !(length("éœ") == 2 && "é" ~ /^[[:lower:]]$/)}' || {
    echo "GNU awk et locale UTF-8 fonctionnelle requis" >&2; exit 1;
}
names=(Fondation Fondation_et_empire Seconde_Fondation)
sources=()
for name in "${names[@]}"; do
    source_file="$root/results/extracted/$name.txt"
    [[ -f "$source_file" && -s "$source_file" ]] || { echo "Source absente/vide : $source_file" >&2; exit 1; }
    iconv -f UTF-8 -t UTF-8 "$source_file" >/dev/null
    sources+=("$source_file")
done
before=$(sha256sum "${sources[@]}")
mkdir -p "$root/results/processed"
report_tmp=$(mktemp "$root/results/report.XXXXXX")
stats_tmp=$(mktemp "$root/results/stats.XXXXXX")
output_tmp=''
cleanup() {
    rm -f -- "$report_tmp" "$stats_tmp"
    if [[ -n "$output_tmp" ]]; then rm -f -- "$output_tmp"; fi
}
trap cleanup EXIT
printf 'Prétraitement conservateur Bash/GNU awk\nLocale : %s\n' "$LC_ALL" > "$report_tmp"
gawk --version | head -n 1 >> "$report_tmp"
printf 'Caractères hors U+000C ; lignes par page. Lignes fusionnées = jonctions avec espace ; tirets réunis comptés séparément.\nArtefacts traités = lignes de pagination, sans double comptage ; marqueurs laissés potentiellement légitimes.\n' >> "$report_tmp"
for name in "${names[@]}"; do
    source_file="$root/results/extracted/$name.txt"
    output_tmp=$(mktemp "$root/results/processed/.stage.XXXXXX")
    gawk -f "$root/scripts/preprocess.awk" "$source_file" > "$output_tmp" 2> "$stats_tmp"
    [[ -s "$output_tmp" ]] || { echo "Sortie vide : $name" >&2; exit 1; }
    iconv -f UTF-8 -t UTF-8 "$output_tmp" >/dev/null
    # Invariant indépendant : mêmes caractères non blancs, dans chaque page,
    # sauf l'unique ligne de pagination finale autorisée. Vérifie aussi la casse,
    # les accents, les tirets et l'absence de déplacement entre pages.
    gawk '
      BEGIN {RS="\f"}
      ARGIND==1 {
        s=$0; sub(/\n?[ \t]*(±[ \t]*[0-9]+[ \t]*±|-[ \t]*[0-9]+[ \t]*-)[ \t]*$/, "",s)
        gsub(/[[:space:]]/,"",s); original[FNR]=s; total=FNR; next
      }
      {s=$0; gsub(/[[:space:]]/,"",s); if(s!=original[FNR]) exit 1; seen=FNR}
      END {if(seen!=total) exit 1}
    ' "$source_file" "$output_tmp" || { echo "Invariant par page violé : $name" >&2; exit 1; }
    mv -- "$output_tmp" "$root/results/processed/$name.txt"
    output_tmp=''
    printf '\n=== %s ===\n' "$name" >> "$report_tmp"
    cat "$stats_tmp" >> "$report_tmp"
done
after=$(sha256sum "${sources[@]}")
[[ "$before" == "$after" ]] || { echo "ERREUR : sources brutes modifiées" >&2; exit 1; }
gawk -F= '/^[a-z_]+=[0-9]+$/ {if(!($1 in sums)) order[++n]=$1; sums[$1]+=$2}
 END {print "\n=== TOTAL CORPUS ==="; for(i=1;i<=n;i++) print order[i] "=" sums[order[i]]}' "$report_tmp" > "$stats_tmp"
cat "$stats_tmp" >> "$report_tmp"
printf '\nSHA-256 sources avant/après : identiques\n%s\nUTF-8 et invariants par page : OK\n' "$before" >> "$report_tmp"
mv -- "$report_tmp" "$root/results/preprocessing_report.txt"
cat "$root/results/preprocessing_report.txt"
