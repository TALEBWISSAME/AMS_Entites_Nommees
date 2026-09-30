"""Audit descriptif des TXT bruts ; aucune correction des sources.

Exécution : python src/entites_nommees/corpus_audit.py
Seul docs/AUDIT_CORPUS.md est écrit. Les seuils sont des conventions
d'observation, pas des règles de prétraitement ou de tokenisation NLP.
"""

from collections import Counter
from hashlib import sha256
from pathlib import Path
import re
import sys
import unicodedata as ud

from corpus_reader import EXTRACTED_DIR, NOVELS, PAGE_SEPARATOR, PROJECT_ROOT

# Référence indépendante : nombres de pages mesurés à la tâche 1.
EXPECTED_PAGES = (108, 116, 120)
FOOTER = re.compile(r"\s*([±–—-])\s*(\d+)\s*\1\s*")
LETTER = r"[^\W\d_]"
CUT = re.compile(rf"{LETTER}+[-‐‑–—]\s*\n[ \t]*{LETTER}+", re.UNICODE)
SIGNS = list(".,;:!?-—–'’\"«»()[]") + ["...", "…"]


def code(value):
    """Extrait court et échappé pour le Markdown, jamais un passage complet."""
    return "`" + value.replace("`", "ˋ").replace("|", "\\|").replace(
        "\n", "\\n").replace("\r", "\\r").replace("\f", "\\f") + "`"


def analyze(text):
    pages = text.split(PAGE_SEPARATOR)
    page_lines = [page.splitlines() for page in pages]
    lines = [line for group in page_lines for line in group]
    forms = text.split()  # Unités séparées par blancs, PAS une tokenisation NLP.
    chars = Counter(text)
    cuts = [(i, m.group()) for i, page in enumerate(pages, 1)
            for m in CUT.finditer(page)]
    endings = [(i, group[-1]) for i, group in enumerate(page_lines, 1) if group]
    footers = [(i, line) for i, line in endings if FOOTER.fullmatch(line)]
    # Diagnostic uniquement : ignorer un pied candidat dans une vue en mémoire
    # pour observer la dernière ligne narrative ; le texte source reste intact.
    boundary_examples = []
    unfinished = lower_start = dialogue = end_hyphen = 0
    for i in range(len(pages) - 1):
        left = [line for line in page_lines[i] if line.strip()]
        right = [line for line in page_lines[i + 1] if line.strip()]
        if not left or not right:
            continue
        last = left[-2] if len(left) > 1 and FOOTER.fullmatch(left[-1]) else left[-1]
        unfinished += bool(last and last.rstrip()[-1] not in '.!?…»"’')
        lower_start += bool(right[0] and right[0][0].islower())
        dialogue += right[0].startswith(('-', '–', '—', '«', '"'))
        end_hyphen += last.rstrip().endswith(('-', '‐', '‑'))
        if len(boundary_examples) < 2:
            boundary_examples.append((i + 1, pages[i][-28:], pages[i + 1][:28:]))
    continuation = sum(
        bool(a.strip() and b.strip() and a.rstrip()[-1] not in '.!?…»"’'
             and b.lstrip()[0].islower())
        for group in page_lines for a, b in zip(group, group[1:])
    )
    margin = Counter(line for group in page_lines for line in
                     (group[:2] + group[-2:]) if line.strip())
    repeated = [(line, count) for line, count in margin.most_common()
                if count >= 2][:8]
    unusual = {c: n for c, n in chars.items()
               if (ud.category(c)[0] in 'CS' or c == '\ufffd'
                   or (ord(c) > 127 and not c.isalpha() and ud.category(c)[0] != 'P'))
               and c not in '\n\f'}
    numbers = Counter(re.findall(r'(?<!\w)\d+(?!\w)', text))
    stats = {
        'Caractères hors séparateurs': len(text) - chars[PAGE_SEPARATOR],
        'Caractères TXT': len(text), 'Lignes': len(lines),
        'Lignes vides': sum(not line.strip() for line in lines),
        'Lignes très courtes (1–10 caractères)': sum(0 < len(line.strip()) <= 10 for line in lines),
        'Mots bruts split()': len(forms), 'Séparateurs': chars[PAGE_SEPARATOR],
        'Séquences de ≥2 espaces ASCII': len(re.findall(r' {2,}', text)),
        'Lignes avec espace/tabulation initial': sum(line.startswith((' ', '\t')) for line in lines),
        'Lignes avec espace/tabulation final': sum(line.endswith((' ', '\t')) for line in lines),
        'Tabulations': chars['\t'], 'Espaces insécables U+00A0': chars['\u00a0'],
        'Espaces insécables fins U+202F': chars['\u202f'],
        'Occurrences inhabituelles (définition ci-dessous)': sum(unusual.values()),
        'Coupures suspectes tiret + retour': len(cuts),
        'Transitions de lignes potentiellement continues': continuation,
        'Frontières après ligne narrative sans ponctuation finale': unfinished,
        'Frontières suivies de minuscule': lower_start,
        'Frontières suivies de marqueur de dialogue': dialogue,
        'Frontières après tiret final narratif': end_hyphen,
        'Pieds numériques encadrés candidats': len(footers),
        'Formes dont le premier caractère est majuscule': sum(x[0].isupper() for x in forms),
        'Formes isupper()': sum(x.isupper() for x in forms),
        'Formes islower()': sum(x.islower() for x in forms),
        'Nombres isolés (occurrences)': sum(numbers.values()),
        'Lignes entièrement numériques': sum(line.strip().isdigit() for line in lines),
    }
    return dict(stats=stats, chars=chars, cuts=cuts, boundaries=boundary_examples,
                repeated=repeated, footers=footers, numbers=numbers, unusual=unusual)


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows])


def report(results, hashes):
    names = [title for title, _, _ in results]
    def metrics(keys):
        return table(['Mesure'] + names + ['Total'],
                     [[key] + [r['stats'][key] for _, _, r in results] +
                      [sum(r['stats'][key] for _, _, r in results)] for key in keys])
    allkeys = list(results[0][2]['stats'])
    parts = ['# Audit du corpus brut', '## Objectif',
             'Observer, mesurer et documenter uniquement. Aucune correction, tokenisation NLP ou extraction d’entités. '
             'Les exigences du professeur (UTF-8, pages impaires, listes futures) sont distinguées des supports de cours '
             'et de nos conventions de mesure. Les seuils et motifs ci-dessous sont nos outils de diagnostic, pas des obligations du professeur.',
             '## Corpus analysé', '\n'.join(f'- `results/extracted/{name}`' for _, name, _ in results),
             '## Extraction actuelle',
             'pdfplumber 0.11.9 ; TXT UTF-8 bruts. `\\f` (U+000C) est le séparateur technique défini dans corpus_reader.py. '
             'Caractères hors séparateurs et lignes par page sont comparables à la tâche 1. Les mots sont estimés par split(), sans nettoyage. '
             'Les majuscules sont mesurées sur ces mêmes formes, ponctuation comprise : premier caractère majuscule, isupper(), islower(). '
             'Ces catégories peuvent se chevaucher et ne détectent pas des personnages.', metrics(allkeys[:9]),
             '## Frontières de pages',
             table(['Roman', 'Séparateurs observés', 'Attendus (tâche 1)', 'Concordance'],
                   [[title, r['stats']['Séparateurs'], n - 1, r['stats']['Séparateurs'] == n - 1]
                    for (title, _, r), n in zip(results, EXPECTED_PAGES)]),
             'Les pages conservées ne sont pas consécutives dans le roman : une page paire manque entre elles. '
             'Une phrase, un dialogue ou un paragraphe peut donc être interrompu, sans que les deux côtés soient à raccorder. '
             'Les compteurs suivants sont des indices, pas une détection certaine des phrases, mots ou paragraphes. '
             'Pour observer la fin narrative, un dernier pied candidat encadré est écarté uniquement dans une vue en mémoire.',
             metrics(allkeys[16:20])]
    for title, _, r in results:
        for page, before, after in r['boundaries']:
            parts.append(f'- {title}, frontière PDF {page}→{page + 1} : {code(before)} → {code(after)}.')
    parts += ['## Retours à la ligne', metrics([allkeys[i] for i in [2, 3, 4, 15]]),
              'Très courte = 1 à 10 caractères après strip() pour la mesure seulement. '
              'Transition candidate = ligne sans .!?…»"’ final suivie d’une ligne commençant par une minuscule, dans une même page. '
              'Cela suggère des retours de mise en page ; les paragraphes réels ne peuvent pas être reconstitués sûrement avec ce seul test.',
              '## Coupures potentielles de mots', metrics([allkeys[14]]),
              'Motif : lettres + tiret (-, ‐, ‑, –, —) + retour de ligne + lettres, dans une même page. '
              'Un composé ou une inversion grammaticale reste possible. Suspect ne signifie pas erreur certaine ; aucun cas n’est corrigé. '
              'Ce motif ne détecte pas toutes les coupures, notamment celles sans tiret.']
    for title, _, r in results:
        parts.append(f'- {title} : ' + (' ; '.join(f'page PDF {p}, {code(s[:45])}' for p, s in r['cuts'][:3]) or 'aucun motif trouvé.'))
    punctuation = set(SIGNS)
    punctuation.update(c for _, _, r in results for c in r['chars'] if ud.category(c).startswith('P'))
    def signs_table(signs):
        rows = []
        for s in signs:
            counts = [r['chars'][s] if len(s) == 1 else r['ellipsis'] for _, _, r in results]
            rows.append([code(s)] + counts + [sum(counts)])
        return table(['Signe'] + names + ['Total'], rows)
    parts += ['## Ponctuation', signs_table(sorted(punctuation)),
              'Les points de « ... » sont inclus dans le compteur du point ; les occurrences de « ... » sont comptées séparément, sans chevauchement. '
              'Les déséquilibres ouvrants/fermants ne prouvent pas une erreur (pages manquantes).',
              '## Apostrophes', signs_table(["'", '’']),
              '## Tirets', signs_table(['-', '–', '—', '‐', '‑'])]
    for title, name, r in results:
        text = (EXTRACTED_DIR / name).read_bytes().decode('utf-8')
        examples = []
        for s in ["'", '’', '-', '–', '—']:
            at = text.find(s)
            if at >= 0:
                examples.append(f'{code(s)} : {code(text[max(0, at-8):at+10])}')
        parts.append(f'- {title} : ' + '; '.join(examples))
    parts += ['Les tirets peuvent marquer dialogues, composés ou inversions : aucune normalisation décidée.',
              '## Casse', metrics(allkeys[21:24]),
              '## Espaces', metrics(allkeys[7:13]),
              'Les séquences de plusieurs espaces sont comptées comme groupes, pas comme nombre d’espaces excédentaires.',
              '## Caractères Unicode',
              'Inventaire ci-dessous : caractères non ASCII, contrôles et symboles. Les lettres accentuées ne sont pas des anomalies. '
              'Le compteur « inhabituel » couvre les catégories Unicode C (contrôle/format/autres), S (symboles), U+FFFD '
              'et les non-ASCII ni lettres ni ponctuation ; il exclut LF et le séparateur technique FF.']
    unicode_chars = {c for _, _, r in results for c in r['chars']
                     if ord(c) > 127 or ud.category(c)[0] in 'CS'} | set('œŒ\ufffd\t\u00a0\u202f')
    rows = []
    for c in sorted(unicode_chars, key=ord):
        counts = [r['chars'][c] for _, _, r in results]
        rows.append([f'U+{ord(c):04X}', code(c) if not c.isspace() else ud.name(c, 'contrôle'),
                     ud.name(c, 'contrôle')] + counts + [sum(counts)])
    parts.append(metrics([allkeys[13]]))
    parts.append(table(['Code', 'Caractère', 'Nom'] + names + ['Total'], rows))
    parts.append(table(['Marqueurs textuels de glyphes PDF'] + names + ['Total'],
                       [['(cid:n)'] + [r['cid'] for _, _, r in results] +
                        [sum(r['cid'] for _, _, r in results)]]))
    parts.append('Les marqueurs `(cid:n)` sont des chaînes ASCII : ils ne seraient pas détectés par un simple inventaire Unicode. '
                 'Les nombres qu’ils contiennent sont inclus dans le comptage numérique brut. '
                 'Exemples courts observés : `l’°uvre` (apostrophe ASCII dans le TXT), `O¶amour-propre` et `(cid:10)°il` dans les deux premiers romans. '
                 'Ces formes suggèrent des glyphes mal extraits, à confirmer au PDF, sans correction. '
                 'Dans Seconde Fondation, `1°` est aussi un emploi légitime du signe degré : le caractère seul ne suffit pas. '
                 'Aucun U+FFFD ni œ/Œ n’est présent ; cette absence ne garantit pas que les ligatures originales ont été fidèlement extraites.')
    parts += ['## Motifs numériques', metrics(allkeys[24:]),
              'Nombres isolés = suites de chiffres non adjacentes à un caractère de mot Unicode. '
              'Ils peuvent désigner dates, quantités ou pages ; aucune suppression automatique.']
    for title, _, r in results:
        parts.append(f'- {title}, dix nombres les plus fréquents : ' + ', '.join(f'{n} ({c})' for n, c in r['numbers'].most_common(10)))
    parts += ['## En-têtes / pieds de page potentiels', metrics([allkeys[20]]),
              'Pied candidat : dernière ligne constituée d’un entier encadré du même signe ±, -, – ou —. '
              'Motifs répétés : égalité exacte dans les deux premières/dernières lignes des pages ; '
              'leur fréquence porte sur ces positions, pas sur tout le roman. Un titre de chapitre est du contenu possible, pas un artefact certain.']
    for title, _, r in results:
        parts.append(f'- {title}, pieds : ' + '; '.join(f'p. PDF {p} {code(s)}' for p, s in r['footers'][:3]))
        parts.append(f'- {title}, marges répétées : ' + ('; '.join(f'{code(s[:45])} ({n})' for s, n in r['repeated']) or 'aucune parmi les motifs retenus.'))
    parts += ['## Problèmes observés',
              'Les mesures révèlent des retours de mise en page, des marqueurs de pagination et des discontinuités de pages. '
              'Les motifs suspects et la typographie sont détaillés ci-dessus ; leur origine exacte (source ou extraction) '
              'nécessite parfois une comparaison au PDF. Une extraction décodable ne garantit pas la fidélité de chaque mot. '
              'Aucune correction ni décision de prétraitement ne découle automatiquement de cet audit.',
              'Contrôle d’intégrité : SHA-256 avant/après identiques pour les trois TXT. Empreintes :',
              '\n'.join(f'- `{name}` : `{digest}`' for name, digest in hashes.items()),
              '## Questions à décider avant prétraitement']
    for question in ['Faut-il fusionner certains retours à la ligne ?',
                     'Faut-il normaliser les apostrophes ?', 'Faut-il normaliser les différents tirets ?',
                     'Comment traiter les frontières entre pages impaires ?',
                     'Comment traiter les mots potentiellement coupés ?',
                     'Quels éléments de ponctuation conserver ?',
                     'Faut-il retirer certains artefacts répétitifs ?',
                     'Comment préserver la casse et les accents utiles aux futures entités ?']:
        parts.append(f'- {question} → À décider')
    return '\n\n'.join(parts) + '\n'


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    results, hashes = [], {}
    for title, pdf_name in NOVELS:
        name = pdf_name.replace('_impaires.pdf', '.txt')
        path = EXTRACTED_DIR / name
        data = path.read_bytes()
        if not data:
            raise ValueError(f'TXT vide : {path}')
        hashes[name] = sha256(data).hexdigest()
        text = data.decode('utf-8', errors='strict')
        result = analyze(text)
        result['ellipsis'] = text.count('...')
        result['cid'] = len(re.findall(r'\(cid:\d+\)', text))
        results.append((title, name, result))
        print(title, result['stats'])
    output = report(results, hashes)
    for name, digest in hashes.items():
        if sha256((EXTRACTED_DIR / name).read_bytes()).hexdigest() != digest:
            raise RuntimeError(f'TXT modifié pendant l’audit : {name}')
    (PROJECT_ROOT / 'docs' / 'AUDIT_CORPUS.md').write_text(output, encoding='utf-8')
    print('TOTAL CORPUS', {key: sum(r['stats'][key] for _, _, r in results)
                           for key in results[0][2]['stats']})
    print('Rapport : docs/AUDIT_CORPUS.md ; intégrité SHA-256 confirmée.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        raise SystemExit(f'Audit impossible : {error}')
