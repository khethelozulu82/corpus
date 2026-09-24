from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main_app.models import UserFavourite, UserSearchHistory, ZuluWord


class DataValidationSystemTests(TestCase):
    def test_data_integrity_across_operations(self):
        """Loading a word, searching for it and favouriting it should never
        change the word's own stored data."""
        word = ZuluWord.objects.create(
            zulu_word='Ubuntu', english_translation='Humanity', part_of_speech='noun',
            cultural_context='A philosophy of shared humanity.',
        )
        user = User.objects.create_user('vuko', password='pass12345')
        self.client.login(username='vuko', password='pass12345')

        self.client.get(reverse('search'), {'q': 'Ubuntu'})
        self.client.post(reverse('add_to_favourites', args=[word.id]))

        word.refresh_from_db()
        self.assertEqual(word.english_translation, 'Humanity')
        self.assertEqual(word.cultural_context, 'A philosophy of shared humanity.')


class ErrorHandlingSystemTests(TestCase):
    def test_error_handling_system(self):
        User.objects.create_user('vuko', password='pass12345')
        self.client.login(username='vuko', password='pass12345')

        # Invalid characters -> friendly validation message, not a 500 error.
        bad_search = self.client.get(reverse('search'), {'q': '###'})
        self.assertEqual(bad_search.status_code, 200)
        self.assertContains(bad_search, 'Please enter a valid word')

        # A word_id that does not exist -> 404, not a crash.
        missing_word = self.client.get(reverse('word_detail', args=[999999]))
        self.assertEqual(missing_word.status_code, 404)

        # Removing a history entry that isn't the user's own -> handled, not a crash.
        other = User.objects.create_user('nomsa', password='pass12345')
        entry = UserSearchHistory.objects.create(user=other, search_query='umuntu')
        response = self.client.post(reverse('remove_history_entry', args=[entry.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserSearchHistory.objects.filter(id=entry.id).exists())  # untouched


class MultiUserSystemTests(TestCase):
    def test_multi_user_data_isolation(self):
        word = ZuluWord.objects.create(zulu_word='Ubuntu', english_translation='Humanity', part_of_speech='noun')
        alice = User.objects.create_user('alice', password='pass12345')
        bob = User.objects.create_user('bob', password='pass12345')

        self.client.login(username='alice', password='pass12345')
        self.client.post(reverse('add_to_favourites', args=[word.id]))
        self.client.get(reverse('search'), {'q': 'Ubuntu'})
        self.client.logout()

        self.client.login(username='bob', password='pass12345')
        bob_favourites = self.client.get(reverse('favourites'))
        bob_history = self.client.get(reverse('history'))

        self.assertEqual(len(bob_favourites.context['favourites']), 0)
        self.assertEqual(len(bob_history.context['history']), 0)
        self.assertTrue(UserFavourite.objects.filter(user=alice, word=word).exists())


class EndToEndWorkflowTests(TestCase):
    def test_complete_user_journey(self):
        # Register.
        register_response = self.client.post(reverse('register'), {
            'username': 'newuser', 'password1': 'a-strong-pass-1', 'password2': 'a-strong-pass-1',
        })
        self.assertEqual(register_response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        word = ZuluWord.objects.create(zulu_word='Sawubona', english_translation='Hello', part_of_speech='greeting')

        # Search.
        self.client.get(reverse('search'), {'q': 'Sawubona'})
        # Favourite.
        self.client.post(reverse('add_to_favourites', args=[word.id]))
        # Check history and favourites both reflect the session.
        self.assertContains(self.client.get(reverse('history')), 'Sawubona')
        self.assertContains(self.client.get(reverse('favourites')), 'Sawubona')
        # View trends without error.
        self.assertEqual(self.client.get(reverse('trends')).status_code, 200)
        # Log out.
        logout_response = self.client.get(reverse('logout'))
        self.assertEqual(logout_response.status_code, 302)
