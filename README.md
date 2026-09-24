# isiZulu Cultural Corpus

A Django web application for exploring isiZulu words and phrases, with English,
Swati and Sotho translations, cultural context, example sentences, and search,
favourites, history and trends features.

University of Zululand, Faculty of Science and Agriculture — module 4CPS212.
Originally a Group 26 project; now maintained by Khethelo Zulu (240107185).

## Documentation

See [`docs/`](docs/) for the project's requirements and design documents:

- `SRS_DOC_1.pdf` — Software Requirements Specification
- `GROUP_26_SDD.docx` — System Design Document (Home & Help pages)
- `Architecture_Strategies.docx` — architecture, data model, module design
- `testPlan-2.docx` — test plan and real test-execution results

All four were revised to match the implementation in this repository; each
document's "Revision note" callouts explain what changed and why.

## Requirements

- Python 3.11+ (project developed and tested on 3.11.9)
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

Then visit `http://127.0.0.1:8000/` and log in (or register a new account).

### Optional environment variables

The app runs with safe local-development defaults out of the box. For any
shared or deployed environment, set:

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django's cryptographic secret key | an insecure local-only key |
| `DJANGO_DEBUG` | `True` / `False` | `True` |
| `DJANGO_ALLOWED_HOSTS` | comma-separated host names | empty |

## Running the tests

```bash
python manage.py test main_app
```

25 tests, covering models, views, integration and system-level workflows —
see `docs/testPlan-2.docx` for the full breakdown and traceability to the SRS.

## Project layout

```
corpus/           Django project settings, root urls
main_app/         the app: models, views, forms, templates' logic, tests
  management/commands/   load_json_data, corpus_stats, populate_zulu_data
  utils/json_loader.py   shared import/export logic (also used by the
                         in-app "Download Database" feature)
  tests/          test_models.py, test_views.py, test_integration.py,
                  test_system.py
templates/        HTML templates
static/           CSS and JavaScript
data.json         seed data — the full corpus, loaded by load_json_data
docs/             requirements & design documents (see above)
```

## Data

`data.json` is the single source of truth for seeding the corpus (139 words).
The in-app "Download Database" button (Search page) generates an up-to-date
JSON export directly from the database, in the same format, so the two never
drift apart.
