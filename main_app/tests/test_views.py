import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main_app.models import UserFavourite, UserSearchHistory, WordPair, ZuluWord


class AuthRequiredTests(TestCase):
    """Every corpus page requires login; anonymous visitors are redirected."""

    def test_home_redirects_anonymous_users_to_login(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('home')}")


class SearchViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('vuko', password='pass12345')
        self.client.login(username='vuko', password='pass12345')
        self.sawubona = ZuluWord.objects.create(
            zulu_word='Sawubona', english_translation='Hello', part_of_speech='greeting',
        )
        self.hamba = ZuluWord.objects.create(
            zulu_word='Hamba kahle', english_translation='Go well', part_of_speech='farewell',
        )

    def test_search_finds_a_word_and_records_history(self):
        response = self.client.get(reverse('search'), {'q': 'Sawubona'})
        self.assertContains(response, 'Sawubona')
        self.assertEqual(UserSearchHistory.objects.filter(user=self.user).count(), 1)

    def test_search_with_no_match_returns_suggestions_not_an_error(self):
        response = self.client.get(reverse('search'), {'q': 'Sawubna'})  # misspelled
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sawubona', response.context['suggestions'])

    def test_two_results_in_one_search_create_a_word_pair(self):
        # Two entries sharing a 3+ character substring, so the same search returns both.
        ZuluWord.objects.create(zulu_word='Ukubonga kakhulu', english_translation='Thank you very much', part_of_speech='phrase')
        ZuluWord.objects.create(zulu_word='Siyabonga', english_translation='We thank you', part_of_speech='phrase')
        self.client.get(reverse('search'), {'q': 'bonga'})
        self.assertTrue(WordPair.objects.exists())

    def test_invalid_characters_are_rejected_with_a_helpful_message(self):
        response = self.client.get(reverse('search'), {'q': '<script>'})
        self.assertContains(response, 'Please enter a valid word')


class FavouritesViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('vuko', password='pass12345')
        self.client.login(username='vuko', password='pass12345')
        self.word = ZuluWord.objects.create(
            zulu_word='Ubuntu', english_translation='Humanity', part_of_speech='noun',
        )

    def test_toggling_favourite_adds_then_removes_it(self):
        url = reverse('add_to_favourites', args=[self.word.id])

        add_response = self.client.post(url)
        self.assertEqual(json.loads(add_response.content)['status'], 'added')
        self.assertTrue(UserFavourite.objects.filter(user=self.user, word=self.word).exists())

        remove_response = self.client.post(url)
        self.assertEqual(json.loads(remove_response.content)['status'], 'removed')
        self.assertFalse(UserFavourite.objects.filter(user=self.user, word=self.word).exists())

    def test_get_request_is_rejected(self):
        response = self.client.get(reverse('add_to_favourites', args=[self.word.id]))
        self.assertEqual(response.status_code, 405)

    def test_anonymous_user_gets_a_login_prompt_not_a_crash(self):
        self.client.logout()
        response = self.client.post(reverse('add_to_favourites', args=[self.word.id]))
        self.assertEqual(response.status_code, 401)
        self.assertIn('log in', json.loads(response.content)['message'])


class HistoryViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('vuko', password='pass12345')
        self.client.login(username='vuko', password='pass12345')

    def test_history_keeps_only_the_5_most_recent_distinct_searches(self):
        for term in ['one', 'two', 'three', 'four', 'five', 'six']:
            UserSearchHistory.objects.create(user=self.user, search_query=term)
        response = self.client.get(reverse('history'))
        self.assertEqual(len(response.context['history']), 5)
        self.assertNotIn('one', [h.search_query for h in response.context['history']])

    def test_repeating_a_search_moves_it_to_the_top_not_a_duplicate(self):
        UserSearchHistory.objects.create(user=self.user, search_query='sawubona')
        UserSearchHistory.objects.create(user=self.user, search_query='hamba kahle')
        UserSearchHistory.objects.create(user=self.user, search_query='sawubona')  # repeat

        response = self.client.get(reverse('history'))
        queries = [h.search_query for h in response.context['history']]
        self.assertEqual(queries, ['sawubona', 'hamba kahle'])

    def test_removing_an_entry_removes_all_repeats_of_that_query(self):
        e1 = UserSearchHistory.objects.create(user=self.user, search_query='sawubona')
        UserSearchHistory.objects.create(user=self.user, search_query='sawubona')
        self.client.post(reverse('remove_history_entry', args=[e1.id]))
        self.assertFalse(UserSearchHistory.objects.filter(user=self.user, search_query='sawubona').exists())


class TrendsViewTests(TestCase):
    def test_total_phrases_only_counts_phrase_like_entries(self):
        User.objects.create_user('vuko', password='pass12345')
        self.client.login(username='vuko', password='pass12345')
        ZuluWord.objects.create(zulu_word='Umuntu', english_translation='Person', part_of_speech='noun')
        ZuluWord.objects.create(
            zulu_word='Umuntu ngumuntu ngabantu', english_translation='A person is a person through other people',
            part_of_speech='proverb',
        )
        response = self.client.get(reverse('trends'))
        self.assertEqual(response.context['total_words'], 2)
        self.assertEqual(response.context['total_phrases'], 1)


class DownloadViewTests(TestCase):
    def test_download_returns_a_json_attachment_of_the_corpus(self):
        User.objects.create_user('vuko', password='pass12345')
        self.client.login(username='vuko', password='pass12345')
        ZuluWord.objects.create(zulu_word='Ubuntu', english_translation='Humanity', part_of_speech='noun')

        response = self.client.get(reverse('download_corpus'))
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')
        self.assertIn('attachment', response['Content-Disposition'])
        payload = json.loads(response.content)
        self.assertEqual(len(payload['words']), 1)
        self.assertEqual(payload['words'][0]['zulu_word'], 'Ubuntu')

    def test_download_requires_login(self):
        response = self.client.get(reverse('download_corpus'))
        self.assertEqual(response.status_code, 302)
