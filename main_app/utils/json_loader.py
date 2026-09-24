"""Import / export of the corpus as JSON.

The same schema is used by the seed file (``data.json``), the
``load_json_data`` management command and the "Download Database" feature:

    {
      "words": [ {<WORD_FIELDS>..., "synonyms": ["<zulu_word>", ...]}, ... ],
      "word_pairs": [ {"word1_zulu": "...", "word2_zulu": "...", "frequency": 1}, ... ]
    }
"""
import json
import os

from django.conf import settings

from main_app.models import WordPair, ZuluWord

WORD_FIELDS = [
    'zulu_word',
    'english_translation',
    'swati_translation',
    'sotho_translation',
    'pronunciation_guide',
    'part_of_speech',
    'cultural_context',
    'example_sentence_zulu',
    'example_sentence_english',
    'example_sentence_swati',
    'example_sentence_sotho',
]


def export_corpus():
    """Return the whole corpus as a JSON-serialisable dict (see module docstring)."""
    words = []
    for word in ZuluWord.objects.prefetch_related('synonyms').order_by('date_added', 'id'):
        entry = {field: getattr(word, field) for field in WORD_FIELDS}
        entry['synonyms'] = [s.zulu_word for s in word.synonyms.all()]
        words.append(entry)

    pairs = [
        {
            'word1_zulu': pair.word1.zulu_word,
            'word2_zulu': pair.word2.zulu_word,
            'frequency': pair.frequency,
        }
        for pair in WordPair.objects.select_related('word1', 'word2').order_by('id')
    ]
    return {'words': words, 'word_pairs': pairs}


def load_words_from_json(json_file_path=None):
    """Load words (and optional word pairs / synonyms) from a JSON file into the database."""
    if json_file_path is None:
        json_file_path = os.path.join(settings.BASE_DIR, 'data.json')

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        words_created = 0
        words_updated = 0

        for word_data in data['words']:
            defaults = {
                field: word_data.get(field, '')
                for field in WORD_FIELDS if field != 'zulu_word'
            }
            defaults['part_of_speech'] = word_data.get('part_of_speech') or 'noun'

            _, created = ZuluWord.objects.update_or_create(
                zulu_word=word_data['zulu_word'],
                defaults=defaults,
            )
            if created:
                words_created += 1
            else:
                words_updated += 1

        # Synonyms (second pass so that every word already exists)
        for word_data in data['words']:
            names = word_data.get('synonyms') or []
            if not names:
                continue
            word = ZuluWord.objects.get(zulu_word=word_data['zulu_word'])
            word.synonyms.set(ZuluWord.objects.filter(zulu_word__in=names))

        pairs_created = 0
        for pair_data in data.get('word_pairs', []):
            try:
                word1 = ZuluWord.objects.get(zulu_word=pair_data['word1_zulu'])
                word2 = ZuluWord.objects.get(zulu_word=pair_data['word2_zulu'])
            except ZuluWord.DoesNotExist:
                print(f"Warning: Could not find words for pair: {pair_data}")
                continue

            _, created = WordPair.objects.get_or_create(
                word1=word1,
                word2=word2,
                defaults={'frequency': pair_data.get('frequency', 1)},
            )
            if created:
                pairs_created += 1

        return {
            'words_created': words_created,
            'words_updated': words_updated,
            'pairs_created': pairs_created,
        }

    except FileNotFoundError:
        print("JSON file not found at:", json_file_path)
        return {'error': 'File not found'}
    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)
        return {'error': 'Invalid JSON'}
    except Exception as e:
        print("Error loading JSON data:", e)
        return {'error': str(e)}
