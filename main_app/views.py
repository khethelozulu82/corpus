import difflib
import json
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .forms import FavouriteSearchForm, SearchForm
from .models import UserFavourite, UserSearchHistory, WordPair, ZuluWord, phrase_filter
from .utils.json_loader import export_corpus

HISTORY_LIMIT = 5
HOME_HISTORY_LIMIT = 4
MAX_PAIR_RESULTS = 10
SUGGESTION_LIMIT = 5


# ---------------------------------------------------------------------------
# Shared context helpers
# ---------------------------------------------------------------------------
def _base_context(request, active_page):
    ctx = {'active_page': active_page}
    if request.user.is_authenticated:
        ctx['favourite_count'] = UserFavourite.objects.filter(user=request.user).count()
    else:
        ctx['favourite_count'] = 0
    return ctx


# ---------------------------------------------------------------------------
# Language switch fallback (?lang=xx&next=/search/)
# ---------------------------------------------------------------------------
def switch_language(request):
    """Fallback language switcher used when the built-in set_language view
    isn't practical (e.g. GET-based links)."""
    lang = request.GET.get('lang', '')
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'

    valid_langs = {code for code, _name in settings.LANGUAGES}
    if lang in valid_langs:
        translation.activate(lang)
        request.session['_language'] = lang

    return redirect(next_url)


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
            messages.success(request, _('Registration successful!'))
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {
        **_base_context(request, 'register'),
        'form': form,
    })


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

    recent_searches = _distinct_recent_searches(request.user, HOME_HISTORY_LIMIT)

    return render(request, 'home.html', {
        **_base_context(request, 'home'),
        'recent_words': recent_words,
        'popular_words': popular_words,
        'recent_searches': recent_searches,
    })


def _distinct_recent_searches(user, limit):
    seen, chosen_ids = set(), []
    rows = (
        UserSearchHistory.objects.filter(user=user)
        .order_by('-search_date', '-id')
        .values_list('id', 'search_query')
    )
    for entry_id, search_query in rows:
        key = search_query.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        chosen_ids.append(entry_id)
        if len(chosen_ids) == limit:
            break

    return (
        UserSearchHistory.objects.filter(id__in=chosen_ids)
        .prefetch_related('search_results')
        .order_by('-search_date', '-id')
    )


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
        **_base_context(request, 'search'),
        'form': form,
        'results': results,
        'query': query,
        'searched': searched,
        'suggestions': suggestions,
    })


def _build_search_conditions(query, search_type='word', exact_match=False):
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
    candidates = {}
    for zulu, english in ZuluWord.objects.values_list('zulu_word', 'english_translation'):
        candidates.setdefault(zulu.lower(), zulu)
        candidates.setdefault(english.lower(), english)
    close = difflib.get_close_matches(query.lower(), list(candidates), n=limit, cutoff=0.6)
    return [candidates[c] for c in close]


def _save_search_history(user, query, results):
    if not results:
        return None
    entry = UserSearchHistory.objects.create(user=user, search_query=query)
    entry.search_results.set(results[:10])
    return entry


def _track_word_pairs(words):
    word_list = list(words)[:MAX_PAIR_RESULTS]
    for i in range(len(word_list)):
        for j in range(i + 1, len(word_list)):
            WordPair.increment_pair_frequency(word_list[i], word_list[j])


def _mark_favourites(user, words):
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
# Word detail
# ---------------------------------------------------------------------------
@login_required
def word_detail(request, word_id):
    word = get_object_or_404(ZuluWord, id=word_id)
    word.is_favourite = UserFavourite.objects.filter(user=request.user, word=word).exists()

    pattern = r'\b' + re.escape(word.zulu_word) + r'\b'

    usage_qs = ZuluWord.objects.filter(example_sentence_zulu__iregex=pattern).exclude(id=word.id)
    usage_count = usage_qs.count() + (1 if re.search(pattern, word.example_sentence_zulu, re.I) else 0)

    phrases = (
        ZuluWord.objects.filter(phrase_filter(), zulu_word__iregex=pattern)
        .exclude(id=word.id).order_by('zulu_word')[:10]
    )

    similar_words = (
        ZuluWord.objects.filter(part_of_speech=word.part_of_speech)
        .exclude(id=word.id).order_by('zulu_word')[:5]
    )

    return render(request, 'word_detail.html', {
        **_base_context(request, 'search'),
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
        **_base_context(request, 'favourites'),
        'favourites': favourite_list,
        'form': form,
        'query': query,
    })


def add_to_favourites(request, word_id):
    if request.method != 'POST':
        return JsonResponse(
            {'status': 'error', 'message': _('Invalid request method. Only POST allowed.')},
            status=405,
        )
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': _('Please log in to save favourites.')},
            status=401,
        )

    try:
        word = ZuluWord.objects.get(id=word_id)
    except ZuluWord.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': _('Word not found.')}, status=404)

    favourite, created = UserFavourite.objects.get_or_create(user=request.user, word=word)
    if created:
        status, message = 'added', _('Added to favourites')
    else:
        favourite.delete()
        status, message = 'removed', _('Removed from favourites')

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
    search_history = _distinct_recent_searches(request.user, HISTORY_LIMIT)
    return render(request, 'history.html', {
        **_base_context(request, 'history'),
        'history': search_history,
    })


@login_required
@require_POST
def remove_history_entry(request, entry_id):
    try:
        entry = UserSearchHistory.objects.get(id=entry_id, user=request.user)
    except UserSearchHistory.DoesNotExist:
        messages.error(request, _('History entry not found.'))
        return redirect('history')

    UserSearchHistory.objects.filter(
        user=request.user, search_query__iexact=entry.search_query
    ).delete()
    messages.success(request, _('Search history entry removed.'))
    return redirect('history')


@login_required
@require_POST
def clear_all_history(request):
    count, _unused = UserSearchHistory.objects.filter(user=request.user).delete()
    messages.success(request, _('Cleared %(count)d history entries.') % {'count': count})
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
        **_base_context(request, 'trends'),
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
    payload = json.dumps(export_corpus(), ensure_ascii=False, indent=2)
    response = HttpResponse(payload, content_type='application/json; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="isiZulu_corpus.json"'
    return response


@login_required
def help_page(request):
    return render(request, 'help.html', _base_context(request, 'help'))


@login_required
def profile(request):
    user = request.user
    favourite_count = UserFavourite.objects.filter(user=user).count()
    search_count = UserSearchHistory.objects.filter(user=user).count()
    recent_searches = UserSearchHistory.objects.filter(user=user).order_by('-search_date')[:5]

    return render(request, 'profile.html', {
        **_base_context(request, 'profile'),
        'user': user,
        'favourite_count': favourite_count,
        'search_count': search_count,
        'recent_searches': recent_searches,
    })


@login_required
def cultural_stories(request):
    return render(request, 'cultural_stories.html', _base_context(request, 'cultural_stories'))