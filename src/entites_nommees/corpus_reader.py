"""Inspection technique uniquement : aucun nettoyage ni traitement NLP."""

from pathlib import Path
import argparse
import sys

try:
    import pdfplumber
except ModuleNotFoundError:
    raise SystemExit(
        "Dépendance absente : installer requirements.txt avec python -m pip install -r requirements.txt"
    )

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = PROJECT_ROOT / "corpus"
EXTRACTED_DIR = PROJECT_ROOT / "results" / "extracted"
PAGE_SEPARATOR = "\f"  # U+000C ajouté entre pages, absent du texte source.
NOVELS = (
    ("Fondation", "Fondation_impaires.pdf"),
    ("Fondation et Empire", "Fondation_et_empire_impaires.pdf"),
    ("Seconde Fondation", "Seconde_Fondation_impaires.pdf"),
)
LABELS = {
    "pages": "Pages",
    "text_pages": "Pages avec texte",
    "empty_pages": "Pages sans texte",
    "characters": "Caractères extraits",
    "lines": "Lignes",
    "raw_words": "Mots bruts approximatifs",
}


def inspect_pdf(path, output_path=None):
    """Inspecter et, sur demande, exporter les chaînes brutes sans correction."""
    if not path.exists():
        raise FileNotFoundError(f"PDF absent : {path}")
    if not path.is_file():
        raise OSError(f"Le chemin ne désigne pas un fichier : {path}")

    texts = []
    empty_pages = []
    with pdfplumber.open(path) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as error:
                raise RuntimeError(
                    f"Extraction impossible à la page PDF {number} : {error}"
                ) from error
            texts.append(text)
            if not text.strip():
                empty_pages.append(number)
            page.close()

    # Un saut de page sépare les pages en mémoire, sans fusionner leurs mots.
    # Ces séparateurs ajoutés ne sont pas comptés comme caractères extraits.
    if any(PAGE_SEPARATOR in text for text in texts):
        raise ValueError("Le texte source contient déjà U+000C : séparateur ambigu.")
    combined = PAGE_SEPARATOR.join(texts)
    statistics = {
        "pages": len(texts),
        "text_pages": len(texts) - len(empty_pages),
        "empty_pages": len(empty_pages),
        "characters": sum(len(text) for text in texts),
        "lines": sum(len(text.splitlines()) for text in texts),
        # split() sépare sur les blancs : estimation technique, PAS du NLP.
        "raw_words": len(combined.split()),
    }
    preview = next((text[:350] for text in texts if text.strip()), "[Aucun texte]")
    if output_path is not None:
        if not statistics["text_pages"]:
            raise ValueError("Export refusé : aucune page avec texte extractible.")
        write_raw_text(output_path, combined, texts)
    return statistics, preview, empty_pages


def write_raw_text(path, text, pages):
    """Écrire en UTF-8 sans conversion des retours de ligne, puis tout relire."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # Une relance régénère le même fichier brut ; aucun PDF n'est écrit.
    with path.open("w", encoding="utf-8", newline="") as stream:
        stream.write(text)
    if not path.is_file() or path.stat().st_size == 0:
        raise OSError(f"Export absent ou vide : {path}")
    data = path.read_bytes()
    restored = data.decode("utf-8", errors="strict")
    if restored != text or restored.split(PAGE_SEPARATOR) != pages:
        raise ValueError(f"Le TXT relu diffère des pages extraites : {path}")
    useful_characters = len(restored) - (len(pages) - 1)
    if useful_characters != sum(len(page) for page in pages):
        raise ValueError(f"Nombre de caractères incohérent : {path}")
    print(f"TXT produit : {path}")
    print(f"Taille du TXT : {len(data)} octets")
    print(f"Caractères TXT : {len(restored)} (dont {len(pages) - 1} séparateurs)")
    print("Vérification : UTF-8 et égalité exacte des pages confirmés")


def print_statistics(statistics):
    for key, label in LABELS.items():
        print(f"{label} : {statistics[key]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", action="store_true",
                        help="Écrire les trois TXT bruts locaux dans results/extracted/.")
    args = parser.parse_args()
    # Évite les erreurs d'encodage de la console Windows et des redirections.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    totals = dict.fromkeys(LABELS, 0)
    successful = 0
    failures = 0
    for title, filename in NOVELS:
        path = CORPUS_DIR / filename
        print(f"\n=== {title} ===\nFichier : {path}")
        try:
            output_path = (
                EXTRACTED_DIR / filename.replace("_impaires.pdf", ".txt")
                if args.export else None
            )
            statistics, preview, empty_pages = inspect_pdf(path, output_path)
        except Exception as error:
            # Frontière CLI : signaler le type et la cause, puis examiner les autres PDF.
            print(f"ERREUR ({type(error).__name__}) : {error}")
            failures += 1
            continue
        successful += 1
        print_statistics(statistics)
        if empty_pages:
            print(f"Pages PDF sans texte (indices à partir de 1) : {empty_pages}")
        if not statistics["text_pages"]:
            print("ALERTE : aucun texte exploitable ; inspection complémentaire nécessaire.")
            failures += 1
        print(f"\nAperçu limité (350 caractères maximum) :\n{preview}")
        for key in totals:
            totals[key] += statistics[key]

    print("\n=== TOTAL CORPUS ===")
    print(f"Romans inspectés : {successful} / {len(NOVELS)}")
    if failures:
        print("ATTENTION : erreur ou absence de texte ; bilan incomplet ou inexploitable.")
    print_statistics(totals)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
