# isiZulu Cultural Corpus

A Django web application for exploring isiZulu words and phrases with English, Swati and Sotho translations, cultural context, example sentences, pronunciation guides, and related linguistic features.


---

## Importance of the system

isiZulu is one of South Africa’s eleven official languages and one of the most widely spoken Nguni languages in the country. Despite this, digital resources that treat isiZulu as a living language — complete with cultural context, proverbs, idioms and everyday usage — remain limited compared with major world languages.

This system addresses that gap by providing:

- **Language preservation and accessibility** — a searchable, structured store of isiZulu vocabulary that includes cultural notes and example sentences, not just bare translations.
- **Multilingual support for southern African languages** — each entry links isiZulu to English, siSwati and Sesotho, supporting cross-language understanding in a region where these languages coexist.
- **Support for research and education** — linguists, students and educators can explore part-of-speech categories, synonyms, co-occurring word pairs and usage trends that would otherwise require manual collection.
- **Cultural depth** — proverbs, idioms, greetings and expressions are recorded with the social and cultural context that makes them meaningful, helping users move beyond word-for-word translation.
- **A practical digital tool** — authentication, personal favourites, search history and an exportable corpus make the resource usable for ongoing study rather than one-off lookups.

In short, the system contributes to the digital presence of an indigenous African language and gives researchers and learners a focused environment in which to work with isiZulu as it is actually used.

## Use of the corpus

The corpus is intended primarily for **researchers of linguistics** and others who want to understand how isiZulu works in practice. Typical uses include:

| Use | How the system supports it |
|-----|----------------------------|
| **Looking up a word or phrase** | Search across isiZulu, English, Swati and Sotho fields, with optional filters for part of speech, exact match, and where to search (word/translation, examples, or cultural context). |
| **Understanding meaning in context** | Each entry can carry cultural context and example sentences in four languages, plus pronunciation and synonyms. |
| **Learning and revision** | Save entries to personal favourites, review recent search history, and use text-to-speech for pronunciation practice. |
| **Linguistic analysis** | Trends page shows overall corpus size, phrase-like entries, word frequencies and word pairs that co-occur in the same search — useful for spotting patterns and associations. |
| **Offline or further research** | Download the full corpus as JSON (login required) for analysis in other tools or for archival use. |
| **Guided exploration** | The Help page documents every feature; the Home page surfaces recently added and most-searched entries as starting points. |

All interactive use requires a logged-in account. Favourites and history are private to each user; the shared corpus content is the same for everyone.

---

## System summary

The isiZulu Cultural Corpus is a single Django monolith. One process serves the HTML pages and handles form processing; data is stored in SQLite. There is no separate API tier. Every page requires an authenticated account.

The live corpus contains **139 entries**. Each entry can include:

- isiZulu word / phrase  
- English, Swati and Sotho translations  
- Pronunciation guide  
- Part of speech (14 categories: noun, verb, adjective, adverb, greeting, farewell, phrase, proverb, idiom, expression, interjection, number, response, unknown)  
- Cultural context  
- Example sentences in isiZulu, English, Swati and Sotho  
- Synonyms (many-to-many)

### Core features

| Feature | Description |
|--------|-------------|
| **Search** | Full-text search across isiZulu, English, Swati and Sotho fields. Filters: *Search in* (word/translation, phrases & examples, or cultural context), *Part of speech*, and *Exact match*. Input is validated (1–100 characters, letters/numbers/spaces/common punctuation). Misspelled queries return up to 5 “Did you mean” suggestions via `difflib`. Every search is recorded in history; co-occurring results are stored as word pairs. |
| **Word detail** | Full entry view with usage, phrases, synonyms, and favourite toggle. |
| **Favourites** | Star button toggles a word into the user’s private favourites via AJAX (no page reload). Favourites page supports searching within saved words. |
| **Search History** | Keeps the 5 most recent distinct queries per user (newest first). Entries can be removed individually or cleared entirely. |
| **Trends** | Aggregate statistics: total words, total phrase-like entries (part-of-speech phrase/proverb/idiom/expression or multi-word entries), word-frequency table and Chart.js bar chart, and the Word Pairs table (pairs that appeared together in the same search, with frequency). |
| **Download** | Login-required view that exports the current database contents as a JSON attachment (same format as the seed file). |
| **Text-to-speech** | Client-side Web Speech API buttons on search results, home lists, and detail pages. |
| **Help & Profile** | Static help guide describing all features; simple user profile page. |

### Data model (4 models)

- **ZuluWord** — core dictionary entry (fields listed above).  
- **WordPair** — tracks pairs of words returned by the same search and their frequency.  
- **UserSearchHistory** — one row per search (user, query, results M2M, timestamp).  
- **UserFavourite** — unique (user, word) pairs with date added.

### Architecture & modules

- **Project**: `corpus/` (settings, root URLs).  
- **App**: `main_app/` — function-based views (18 functions), forms, models, admin, management commands (`load_json_data`, `corpus_stats`, `populate_zulu_data`), and shared JSON import/export utilities.  
- **Templates**: 15 HTML files extending `base.html`.  
- **Static**: CSS and JavaScript (favourite-star AJAX, Chart.js trends chart, Web Speech API).  

Full architecture, data-model details, module responsibilities and key design decisions are documented in `docs/Architecture_Strategies.docx`. Page-level design for Home and Help is in `docs/GROUP_26_SDD.docx`. Functional requirements are in `docs/SRS_DOC_1.pdf`. Automated test results are in `docs/testPlan-2.docx`.

---

## Requirements

- Python 3.11+ (developed on 3.11.9; verified on 3.12.3)  
- Django 5.2.6 (see `requirements.txt`)

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py load_json_data # loads the 139-word corpus from data.json
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in (or register).

### Optional environment variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `DJANGO_SECRET_KEY` | Cryptographic secret key | insecure local-only key |
| `DJANGO_DEBUG` | `True` / `False` | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated host names | empty |

## Running the tests

```bash
python manage.py test main_app
```

25 automated tests (models, views, integration, system) — all passing. See `docs/testPlan-2.docx` for the full case list and SRS traceability.

## Project layout

```
corpus/                 Django project settings & root URLs
main_app/               Models, views, forms, admin, tests, management commands
  management/commands/  load_json_data, corpus_stats, populate_zulu_data
  utils/json_loader.py  Shared import/export (also used by in-app Download)
  tests/                test_models, test_views, test_integration, test_system
templates/              HTML templates
static/                 CSS, JavaScript, images
data.json               Seed corpus (139 words)
docs/                   SRS, SDD, Architecture Strategies, Test Plan
```

## Data

`data.json` is the single seed source. The in-app **Download Database** action generates a fresh JSON export directly from the live database in the same format, so seed and export stay consistent.
