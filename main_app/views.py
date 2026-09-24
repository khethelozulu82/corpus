import difflib
import json
import re

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import FavouriteSearchForm, SearchForm
from .models import UserFavourite, UserSearchHistory, WordPair, ZuluWord, phrase_filter
from .utils.json_loader import export_corpus

HISTORY_LIMIT = 5        # distinct searches shown on the History page
MAX_PAIR_RESULTS = 10    # results per search that are used to update word pairs
SUGGESTION_LIMIT = 5     # "Did you mean" suggestions shown when a search finds nothing


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
def custom_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
@login_required
def home(request):
    recent_words = list(ZuluWord.objects.order_by('-date_added', '-id')[:5])
    popular_words = list(
        ZuluWord.objects.annotate(search_count=Count('usersearchhistory'))
        .order_by('-search_count', 'zulu_word')[:5]
    )
    _mark_favourites(request.user, recent_words + popular_words)

    return render(request, 'home.html', {
        'recent_words': recent_words,
        'popular_words': popular_words,
    })


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
@login_required
def search(request):
    form = SearchForm(request.GET or None)
    results = []
    suggestions = []
    query = request.GET.get('q', '').strip()
    searched = form.is_valid()

    if searched:
        query = form.cleaned_data['q']
        conditions = _build_search_conditions(
            query,
            form.cleaned_data.get('search_type') or 'word',
            form.cleaned_data.get('exact_match', False),
        )
        matches = ZuluWord.objects.filter(conditions)
        if form.cleaned_data.get('pos'):
            matches = matches.filter(part_of_speech=form.cleaned_data['pos'])

        results = list(matches.order_by('zulu_word'))
        if results:
            _save_search_history(request.user, query, results)
            _track_word_pairs(results)
            _mark_favourites(request.user, results)
        else:
            suggestions = _suggest_words(query)

    return render(request, 'search.html', {
        'form': form,
        'results': results,
        'query': query,
        'searched': searched,
        'suggestions': suggestions,
    })


def _build_search_conditions(query, search_type='word', exact_match=False):
    """Build the Q object for a search.

    Short queries (< 3 characters) and "exact match" use a case-insensitive
    exact comparison; longer queries use a case-insensitive "contains".
    ``search_type`` widens the fields searched: 'phrase' adds the example
    sentences, 'definition' adds the cultural context.
    """
    if not query:
        return None

    lookup = 'iexact' if (exact_match or len(query) < 3) else 'icontains'

    fields = ['zulu_word', 'english_translation', 'swati_translation', 'sotho_translation']
    if search_type == 'phrase':
        fields += [
            'example_sentence_zulu', 'example_sentence_english',
            'example_sentence_swati', 'example_sentence_sotho',
        ]
    elif search_type == 'definition':
        fields += ['cultural_context']

    conditions = Q()
    for field in fields:
        conditions |= Q(**{f'{field}__{lookup}': query})
    return conditions


def _suggest_words(query, limit=SUGGESTION_LIMIT):
    """Fuzzy "Did you mean" suggestions for a search that found nothing."""
    candidates = {}
    for zulu, english in ZuluWord.objects.values_list('zulu_word', 'english_translation'):
        candidates.setdefault(zulu.lower(), zulu)
        candidates.setdefault(english.lower(), english)
    close = difflib.get_close_matches(query.lower(), list(candidates), n=limit, cutoff=0.6)
    return [candidates[c] for c in close]


def _save_search_history(user, query, results):
    """Record a search (one row per search event) with its first 10 results."""
    if not results:
        return None
    entry = UserSearchHistory.objects.create(user=user, search_query=query)
    entry.search_results.set(results[:10])
    return entry


def _track_word_pairs(words):
    """Count which entries are returned together (first MAX_PAIR_RESULTS only)."""
    word_list = list(words)[:MAX_PAIR_RESULTS]
    for i in range(len(word_list)):
        for j in range(i + 1, len(word_list)):
            WordPair.increment_pair_frequency(word_list[i], word_list[j])


def _mark_favourites(user, words):
    """Set ``is_favourite`` on each word for the given user."""
    words = list(words)
    if not words:
        return
    favourite_ids = set(
        UserFavourite.objects.filter(user=user, word_id__in=[w.id for w in words])
        .values_list('word_id', flat=True)
    )
    for word in words:
        word.is_favourite = word.id in favourite_ids


# ---------------------------------------------------------------------------
# Word detail (word usage, translations, phrases, synonyms)
# ---------------------------------------------------------------------------
@login_required
def word_detail(request, word_id):
    word = get_object_or_404(ZuluWord, id=word_id)
    word.is_favourite = UserFavourite.objects.filter(user=request.user, word=word).exists()

    pattern = r'\b' + re.escape(word.zulu_word) + r'\b'

    # Word usage: other entries whose example sentence contains this word
    usage_qs = ZuluWord.objects.filter(example_sentence_zulu__iregex=pattern).exclude(id=word.id)
    usage_count = usage_qs.count() + (1 if re.search(pattern, word.example_sentence_zulu, re.I) else 0)

    # Phrases: phrase-like entries (proverbs, idioms, ...) containing this word
    phrases = (
        ZuluWord.objects.filter(phrase_filter(), zulu_word__iregex=pattern)
        .exclude(id=word.id).order_by('zulu_word')[:10]
    )

    similar_words = (
        ZuluWord.objects.filter(part_of_speech=word.part_of_speech)
        .exclude(id=word.id).order_by('zulu_word')[:5]
    )

    return render(request, 'word_detail.html', {
        'word': word,
        'usage_count': usage_count,
        'usage_examples': usage_qs.order_by('zulu_word')[:5],
        'phrases': phrases,
        'synonyms': word.synonyms.all().order_by('zulu_word'),
        'similar_words': similar_words,
    })


# ---------------------------------------------------------------------------
# Favourites
# ---------------------------------------------------------------------------
@login_required
def favourites(request):
    form = FavouriteSearchForm(request.GET or None)
    favourite_list = (
        UserFavourite.objects.filter(user=request.user)
        .select_related('word').order_by('-date_added')
    )
    query = ''
    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            favourite_list = favourite_list.filter(
                Q(word__zulu_word__icontains=query)
                | Q(word__english_translation__icontains=query)
                | Q(word__swati_translation__icontains=query)
                | Q(word__sotho_translation__icontains=query)
            )

    return render(request, 'favourites.html', {
        'favourites': favourite_list,
        'form': form,
        'query': query,
    })


def add_to_favourites(request, word_id):
    """Toggle a word in the current user's favourites (AJAX, POST only)."""
    if request.method != 'POST':
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid request method. Only POST allowed.'},
            status=405,
        )
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Please log in to save favourites.'},
            status=401,
        )

    try:
        word = ZuluWord.objects.get(id=word_id)
    except ZuluWord.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Word not found.'}, status=404)

    favourite, created = UserFavourite.objects.get_or_create(user=request.user, word=word)
    if created:
        status, message = 'added', 'Added to favourites'
    else:
        favourite.delete()
        status, message = 'removed', 'Removed from favourites'

    return JsonResponse({
        'status': status,
        'message': message,
        'word_id': word_id,
        'word_name': word.zulu_word,
    })


# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------
@login_required
def history(request):
    """Most recent distinct searches, newest first."""
    seen, chosen_ids = set(), []
    rows = (
        UserSearchHistory.objects.filter(user=request.user)
        .order_by('-search_date', '-id').values_list('id', 'search_query')
    )
    for entry_id, search_query in rows:
        key = search_query.strip().lower()
        if key in seen:
            continue  # a repeated search only appears once (at its latest position)
        seen.add(key)
        chosen_ids.append(entry_id)
        if len(chosen_ids) == HISTORY_LIMIT:
            break

    search_history = (
        UserSearchHistory.objects.filter(id__in=chosen_ids)
        .prefetch_related('search_results').order_by('-search_date', '-id')
    )
    return render(request, 'history.html', {'history': search_history})


@login_required
@require_POST
def remove_history_entry(request, entry_id):
    """Remove a search from the history (all repeats of that query as well)."""
    try:
        entry = UserSearchHistory.objects.get(id=entry_id, user=request.user)
    except UserSearchHistory.DoesNotExist:
        messages.error(request, 'History entry not found.')
        return redirect('history')

    UserSearchHistory.objects.filter(
        user=request.user, search_query__iexact=entry.search_query
    ).delete()
    messages.success(request, 'Search history entry removed.')
    return redirect('history')


@login_required
@require_POST
def clear_all_history(request):
    count, _ = UserSearchHistory.objects.filter(user=request.user).delete()
    messages.success(request, f'Cleared {count} history entries.')
    return redirect('history')


# ---------------------------------------------------------------------------
# Trends
# ---------------------------------------------------------------------------
@login_required
def trends(request):
    word_frequency = (
        ZuluWord.objects.annotate(search_count=Count('usersearchhistory'))
        .order_by('-search_count', 'zulu_word')[:10]
    )
    word_pairs = (
        WordPair.objects.select_related('word1', 'word2')
        .order_by('-frequency', 'id')[:10]
    )

    return render(request, 'trends.html', {
        'word_frequency': word_frequency,
        'word_pairs': word_pairs,
        'total_words': ZuluWord.objects.count(),
        'total_phrases': ZuluWord.objects.filter(phrase_filter()).count(),
        'total_users': User.objects.count(),
        'total_searches': UserSearchHistory.objects.count(),
    })


# ---------------------------------------------------------------------------
# Download, help, profile, cultural stories
# ---------------------------------------------------------------------------
@login_required
def download_corpus_data(request):
    """Download the whole corpus (generated from the database) as a JSON file."""
    payload = json.dumps(export_corpus(), ensure_ascii=False, indent=2)
    response = HttpResponse(payload, content_type='application/json; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="isiZulu_corpus.json"'
    return response


@login_required
def help_page(request):
    return render(request, 'help.html')


@login_required
def profile(request):
    user = request.user
    favourite_count = UserFavourite.objects.filter(user=user).count()
    search_count = UserSearchHistory.objects.filter(user=user).count()
    recent_searches = UserSearchHistory.objects.filter(user=user).order_by('-search_date')[:5]

    return render(request, 'profile.html', {
        'user': user,
        'favourite_count': favourite_count,
        'search_count': search_count,
        'recent_searches': recent_searches,
    })


@login_required
def cultural_stories(request):
    return render(request, 'cultural_stories.html')
