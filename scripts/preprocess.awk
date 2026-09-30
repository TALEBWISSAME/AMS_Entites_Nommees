# GNU awk, locale UTF-8. Une unité de lecture = une page extraite.
# Aucun état de fusion ne survit à une frontière U+000C.
BEGIN {
    RS = "\f"
    split("années-lumière vous-même vous-mêmes Dites-moi dites-moi eux-mêmes au-dessus au-dessous diriez-vous", words, " ")
    for (i in words) allowed[words[i]] = 1
}
function pagination(s) {
    return s ~ /^[ \t]*(±[ \t]*[0-9]+[ \t]*±|-[ \t]*[0-9]+[ \t]*-)[ \t]*$/
}
function structural(s) {
    return s ~ /^[ \t]*$/ || s ~ /^[ \t]/ || s ~ /^[-–—«"']/ ||
           s ~ /^[[:upper:][:digit:] .:!?-]+$/
}
function hyphen_pair(a,b, x,y) {
    if (!match(a, /[[:alpha:]]+-$/)) return 0
    x = substr(a, RSTART)
    if (!match(b, /^[[:alpha:]]+/)) return 0
    y = substr(b, 1, RLENGTH)
    return (x y) in allowed
}
function continuation(a,b) {
    # Choix très restreint : préposition finale + déterminant initial.
    # Exclure dialogues, titres, espaces marginaux et lignes courtes.
    return !structural(a) && !structural(b) && length(a) >= 25 &&
           a ~ / (par|dans|avec|sans|sous|chez|vers|entre)$/ &&
           b ~ /^(le|la|les|un|une|des|du|de|ce|cette|ces|son|sa|ses|leur|leurs) /
}
function emit_metric(key,value) { print key "=" (value+0) > "/dev/stderr" }
{
    before_chars += length($0)
    n = split($0, line, "\n")
    if ($0 == "") n = 0
    before_lines += n
    # Pagination : ligne entière, seulement dernière ligne de la page.
    last = n
    while (last > 0 && line[last] ~ /^[ \t]*$/) last--
    removed = 0
    if (last > 0 && pagination(line[last])) {
        removed = last
        pagination_removed++
        if (trace && pagination_removed <= 2)
            print "pagination page=" NR " ligne=" last > "/dev/stderr"
    }
    out = ""
    count = 0
    previous = ""
    for (i=1; i<=n; i++) {
        if (i == removed) continue
        current = line[i]
        # On compare les lignes originales, pas la longueur d'un bloc déjà fusionné.
        join = 0
        if (count && previous ~ /[[:alpha:]]+-$/ && current ~ /^[[:alpha:]]/) {
            if (hyphen_pair(previous,current)) {
                join=2
                hyphens_joined++
            } else { hyphens_ambiguous++; ambiguous++ }
        } else if (count && continuation(previous,current)) {
            join=1
            merged++
        } else if (count && !structural(previous) && !structural(current) &&
                   previous !~ /[.!?…:;"»]$/) ambiguous++
        if (join) {
            out = out (join == 1 ? " " : "") current
            if (trace && merged+hyphens_joined <= 4)
                print "fusion page=" NR " lignes=" i-1 "," i " type=" join > "/dev/stderr"
        } else {
            out = out (count ? "\n" : "") current
            count++
        }
        previous = current
    }
    # Compteurs de marqueurs conservés, pas un nombre certain d'erreurs.
    temp=out; cid += gsub(/\(cid:[0-9]+\)/,"",temp)
    temp=out; pilcrow += gsub(/¶/,"",temp)
    temp=out; degree += gsub(/°/,"",temp)
    temp=out; plusminus += gsub(/±/,"",temp)
    after_chars += length(out)
    after_lines += count
    # RT reproduit exactement chaque frontière, sans ajouter de séparateur final.
    printf "%s%s", out, RT
    if (RT != "") boundaries++
}
END {
    emit_metric("caracteres_avant",before_chars)
    emit_metric("caracteres_apres",after_chars)
    emit_metric("lignes_avant",before_lines)
    emit_metric("lignes_apres",after_lines)
    emit_metric("frontieres_preservees",boundaries)
    emit_metric("pagination_supprimee",pagination_removed)
    emit_metric("lignes_fusionnees",merged)
    emit_metric("lignes_conservees",after_lines)
    emit_metric("tirets_reunis",hyphens_joined)
    emit_metric("tirets_ambigus",hyphens_ambiguous)
    emit_metric("artefacts_certains_traites",pagination_removed)
    emit_metric("artefacts_laisses",cid+pilcrow+degree+plusminus)
    emit_metric("cid_laisses",cid)
    emit_metric("pilcrows_laisses",pilcrow)
    emit_metric("degres_laisses",degree)
    emit_metric("plusmoins_laisses",plusminus)
    emit_metric("cas_ambigus",ambiguous)
}
