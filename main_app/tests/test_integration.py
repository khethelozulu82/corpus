from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main_app.models import UserFavourite, ZuluWord


class UserWorkflowIntegrationTests(TestCase):
    """Search, Favourites and History working together, the way a user experiences them."""

    def setUp(self):
        self.user = User.objects.create_user('vuko', password='pass12345')
        self.client.login(username='vuko', password='pass12345')
        self.word = ZuluWord.objects.create(
            zulu_word='Sawubona', english_translation='Hello', part_of_speech='greeting',
        )

    def test_complete_search_workflow(self):
        # 1. Search for a word.
        search_response = self.client.get(reverse('search'), {'q': 'Sawubona'})
        self.assertContains(search_response, 'Sawubona')

        # 2. The search is recorded in History.
        history_response = self.client.get(reverse('history'))
        self.assertEqual(len(history_response.context['history']), 1)

        # 3. The word's detail page reflects that it is not yet a favourite.
        detail_response = self.client.get(reverse('word_detail', args=[self.word.id]))
        self.assertFalse(detail_response.context['word'].is_favourite)

    def test_favourites_workflow(self):
        # 1. Favourite a word from the search results.
        self.client.post(reverse('add_to_favourites', args=[self.word.id]))
        self.assertTrue(UserFavourite.objects.filter(user=self.user, word=self.word).exists())

        # 2. It now shows on the Favourites page.
        fav_response = self.client.get(reverse('favourites'))
        self.assertContains(fav_response, 'Sawubona')

        # 3. And the word detail page now shows it as a favourite.
        detail_response = self.client.get(reverse('word_detail', args=[self.word.id]))
        self.assertTrue(detail_response.context['word'].is_favourite)

        # 4. Searching the favourites panel for it still finds it; a made-up term does not.
        self.assertContains(self.client.get(reverse('favourites'), {'q': 'Sawu'}), 'Sawubona')
        self.assertNotContains(self.client.get(reverse('favourites'), {'q': 'xyz'}), 'Sawubona')
