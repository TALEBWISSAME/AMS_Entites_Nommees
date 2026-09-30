"""Générer LP depuis L par raffinements déterministes, sans NER externe."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import argparse
import csv
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results" / "lists" / "liste_L.txt"
DEFAULT_OUTPUT = ROOT / "results" / "lists" / "liste_LP.txt"
DEFAULT_STATS = ROOT / "results" / "lists" / "liste_LP_stats.txt"

TITLE_WORDS = {
    "M",
    "Monsieur",
    "Madame",
    "Mademoiselle",
    "Docteur",
    "Dr",
    "Général",
    "Commandant",
    "Capitaine",
    "Colonel",
    "Major",
    "Maître",
    "Amiral",
    "Commodore",
    "Prince",
    "Princesse",
    "Roi",
    "Reine",
    "Empereur",
    "Impératrice",
    "Dame",
    "Seigneur",
}

# Ressource locale courte de mots grammaticaux et narratifs fréquents. Elle sert à
# réduire le bruit de début de phrase, sans prétendre être un antidictionnaire.
INITIAL_REJECT = {
    "A",
    "Ah",
    "Alors",
    "Après",
    "Au",
    "Aucun",
    "Aucune",
    "Aussi",
    "Avec",
    "Ainsi",
    "Allons",
    "Bon",
    "Bref",
    "Car",
    "Ce",
    "C'est",
    "C'était",
    "Cela",
    "Cette",
    "Ces",
    "Cet",
    "Comme",
    "Comment",
    "Dans",
    "De",
    "Des",
    "Donc",
    "Du",
    "Elle",
    "Elles",
    "En",
    "Encore",
    "Et",
    "Eh",
    "Il",
    "Ils",
    "Je",
    "J'ai",
    "J'étais",
    "La",
    "Le",
    "Les",
    "Lorsque",
    "Lui",
    "Mais",
    "Même",
    "Ne",
    "Non",
    "Nous",
    "On",
    "Or",
    "Oui",
    "Par",
    "Parce",
    "Pas",
    "Pendant",
    "Peut-être",
    "Plus",
    "Pour",
    "Pourquoi",
    "Puis",
    "Quand",
    "Que",
    "Quel",
    "Quelle",
    "Qui",
    "Quoi",
    "Sans",
    "Si",
    "Sa",
    "Ses",
    "Son",
    "Sur",
    "Tout",
    "Toute",
    "Très",
    "Tu",
    "Un",
    "Une",
    "Vous",
    "Voilà",
    "Votre",
}

NON_PERSON_TERMS = {
    "Académie",
    "Anacreon",
    "Anacréon",
    "Assemblée",
    "Association",
    "Bibliothèque",
    "Conseil",
    "Encyclopedia",
    "Encyclopédie",
    "Empire",
    "Fondation",
    "Fondations",
    "Galaxie",
    "Galactique",
    "Hôtel",
    "Korell",
    "Mairie",
    "Palais",
    "Partie",
    "Planète",
    "Plan",
    "Premier",
    "République",
    "Secteur",
    "Seconde",
    "Seldonien",
    "Terminus",
    "Trantor",
    "Université",
    "Majesté",
    "Impériale",
    "Marchand",
    "Orateur",
    "ENCYCLOPEDIA",
    "GALACTICA",
    "CHAPITRE",
    "PARTIE",
}

AMBIGUOUS_SINGLE_HINTS = {
    "Sire",
    "Patricien",
    "Maire",
    "Docteur",
    "Général",
    "Capitaine",
    "Commandant",
    "Commodore",
}

ARTIFACT_RE = re.compile(r"\(cid:\d+\)|[¶°\\\[\]_]")
ROMAN_RE = re.compile(r"^[IVXLCDM]+$")


@dataclass(frozen=True)
class LEntry:
    n: int
    form: str
    frequency: int


@dataclass(frozen=True)
class Decision:
    entry: LEntry
    status: str
    reason: str


def read_l(path: Path) -> list[LEntry]:
    data = path.read_text(encoding="utf-8")
    rows: list[LEntry] = []
    reader = csv.DictReader(data.splitlines(), delimiter="\t")
    required = {"n", "forme", "frequence"}
    if set(reader.fieldnames or []) != required:
        raise ValueError("format L attendu: n<TAB>forme<TAB>frequence")
    for row in reader:
        form = row["forme"]
        if not form:
            continue
        rows.append(LEntry(int(row["n"]), form, int(row["frequence"])))
    return rows


def is_upper_initial(token: str) -> bool:
    return bool(token) and token[0].isupper()


def is_name_token(token: str) -> bool:
    if not token or token in INITIAL_REJECT:
        return False
    if ARTIFACT_RE.search(token) or any(ch.isdigit() for ch in token):
        return False
    if ROMAN_RE.fullmatch(token):
        return False
    return is_upper_initial(token)


def all_caps_structural(tokens: list[str]) -> bool:
    letters = [token for token in tokens if any(ch.isalpha() for ch in token)]
    return bool(letters) and all(token.upper() == token for token in letters)


def has_uppercase_block(tokens: list[str]) -> bool:
    return any(
        len(token) > 1 and token.upper() == token and any(ch.isalpha() for ch in token)
        for token in tokens
    )


def is_elided_noise(token: str) -> bool:
    return bool(re.match(r"^(C|J)'", token))


def classify(entry: LEntry) -> Decision:
    tokens = entry.form.split()
    if entry.n not in {1, 2, 3} or entry.n != len(tokens):
        return Decision(entry, "rejet", "structure_l_invalide")
    if ARTIFACT_RE.search(entry.form):
        return Decision(entry, "rejet", "artefact")
    if any(any(ch.isdigit() for ch in token) for token in tokens):
        return Decision(entry, "rejet", "contient_nombre")
    if entry.n > 1 and all_caps_structural(tokens):
        return Decision(entry, "rejet", "structure_majuscule_titre")
    if tokens[0] in INITIAL_REJECT or is_elided_noise(tokens[0]):
        return Decision(entry, "rejet", "debut_mot_grammatical")
    if any(token in NON_PERSON_TERMS for token in tokens):
        return Decision(entry, "rejet", "indice_non_personne")
    if entry.n > 1 and has_uppercase_block(tokens):
        return Decision(entry, "rejet", "structure_majuscule_titre")

    if entry.n == 1:
        token = tokens[0]
        if token in AMBIGUOUS_SINGLE_HINTS:
            return Decision(entry, "ambigu", "titre_ou_fonction_sans_nom")
        if is_name_token(token) and entry.frequency >= 2:
            return Decision(entry, "retenu", "unigramme_majuscule_frequent")
        if is_name_token(token):
            return Decision(entry, "ambigu", "unigramme_rare")
        return Decision(entry, "rejet", "unigramme_non_nominal")

    if tokens[0] in TITLE_WORDS:
        if (
            len(tokens) >= 2
            and all(is_name_token(token) for token in tokens[1:])
            and not any("'" in token or "’" in token for token in tokens[1:])
        ):
            return Decision(entry, "retenu", "titre_suivi_nom")
        return Decision(entry, "ambigu", "titre_sans_nom_clair")

    name_like = [is_name_token(token) for token in tokens]
    if all(name_like):
        if any(token in TITLE_WORDS for token in tokens[1:]):
            return Decision(entry, "ambigu", "titre_interne")
        if entry.n == 3 and entry.frequency < 2:
            return Decision(entry, "ambigu", "trigramme_nominal_rare")
        return Decision(entry, "retenu", f"{entry.n}gramme_nominal_majuscule")
    if name_like[0] and any(token and token[0].islower() for token in tokens[1:]):
        return Decision(entry, "rejet", "nom_suivi_contexte")
    if name_like[0]:
        return Decision(entry, "ambigu", "sequence_nominale_partielle")
    return Decision(entry, "rejet", "sequence_non_personne")


def generate(input_l: Path, output_lp: Path, output_stats: Path) -> tuple[list[Decision], str]:
    input_hash_before = sha256(input_l.read_bytes()).hexdigest()
    entries = read_l(input_l)
    decisions = [classify(entry) for entry in entries]
    retained = [decision for decision in decisions if decision.status == "retenu"]
    retained.sort(key=lambda item: (-item.entry.frequency, item.entry.form, item.entry.n))

    output_lp.parent.mkdir(parents=True, exist_ok=True)
    with output_lp.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["forme", "frequence", "n", "preuve"])
        for decision in retained:
            writer.writerow([
                decision.entry.form,
                decision.entry.frequency,
                decision.entry.n,
                decision.reason,
            ])

    status_counts = Counter(decision.status for decision in decisions)
    reason_counts = Counter(decision.reason for decision in decisions)
    retained_n = Counter(decision.entry.n for decision in retained)
    rejected_n = Counter(decision.entry.n for decision in decisions if decision.status == "rejet")
    ambiguous_n = Counter(decision.entry.n for decision in decisions if decision.status == "ambigu")
    total_occurrences = sum(decision.entry.frequency for decision in retained)
    artifact_rejects = reason_counts["artefact"]
    variants = count_case_variants([decision.entry.form for decision in retained])

    with output_stats.open("w", encoding="utf-8", newline="") as stream:
        stream.write("Génération de LP\n")
        stream.write("Source: results/lists/liste_L.txt\n")
        stream.write("Format liste: forme<TAB>frequence<TAB>n<TAB>preuve\n")
        stream.write("Méthode: filtrage déterministe de L, sans antidictionnaire externe ni NER\n\n")
        stream.write(f"lignes_l={len(entries)}\n")
        stream.write(f"candidats_examines={len(decisions)}\n")
        stream.write(f"retenus={status_counts['retenu']}\n")
        stream.write(f"rejetes={status_counts['rejet']}\n")
        stream.write(f"ambigus={status_counts['ambigu']}\n")
        stream.write(f"occurrences_lp={total_occurrences}\n")
        stream.write(f"retenus_n1={retained_n[1]}\n")
        stream.write(f"retenus_n2={retained_n[2]}\n")
        stream.write(f"retenus_n3={retained_n[3]}\n")
        stream.write(f"rejetes_n1={rejected_n[1]}\n")
        stream.write(f"rejetes_n2={rejected_n[2]}\n")
        stream.write(f"rejetes_n3={rejected_n[3]}\n")
        stream.write(f"ambigus_n1={ambiguous_n[1]}\n")
        stream.write(f"ambigus_n2={ambiguous_n[2]}\n")
        stream.write(f"ambigus_n3={ambiguous_n[3]}\n")
        stream.write(f"artefacts_rejetes={artifact_rejects}\n")
        stream.write(f"variantes_casse_potentielles={variants}\n")
        stream.write(f"sha256_l_avant={input_hash_before}\n")
        stream.write(f"sha256_l_apres={sha256(input_l.read_bytes()).hexdigest()}\n\n")
        stream.write("raisons\n")
        for reason, count in sorted(reason_counts.items()):
            stream.write(f"{reason}\t{count}\n")

    return decisions, output_stats.read_text(encoding="utf-8")


def count_case_variants(forms: list[str]) -> int:
    groups: dict[str, set[str]] = {}
    for form in forms:
        groups.setdefault(form.casefold(), set()).add(form)
    return sum(1 for variants in groups.values() if len(variants) > 1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stats", type=Path, default=DEFAULT_STATS)
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        _, stats = generate(args.input, args.output, args.stats)
    except (OSError, ValueError) as error:
        print(f"Erreur: {error}", file=sys.stderr)
        return 1
    print(stats, end="")
    print("Sorties UTF-8 : OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
