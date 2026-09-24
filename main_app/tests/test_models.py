from django.contrib.auth.models import User
from django.test import TestCase

from main_app.models import UserFavourite, UserSearchHistory, WordPair, ZuluWord, phrase_filter


class ZuluWordModelTests(TestCase):
    def test_string_representation(self):
        word = ZuluWord.objects.create(
            zulu_word='Sawubona', english_translation='Hello', part_of_speech='greeting'
        )
        self.assertEqual(str(word), 'Sawubona')

    def test_phrase_filter_matches_phrase_types_and_multi_word_entries(self):
        proverb = ZuluWord.objects.create(
            zulu_word='Ukhamba oluhle', english_translation='A well-behaved child',
            part_of_speech='proverb',
        )
        noun = ZuluWord.objects.create(
            zulu_word='Umuntu', english_translation='Person', part_of_speech='noun',
        )
        matches = ZuluWord.objects.filter(phrase_filter())
        self.assertIn(proverb, matches)
        self.assertNotIn(noun, matches)


class WordPairModelTests(TestCase):
    def setUp(self):
        self.w1 = ZuluWord.objects.create(zulu_word='Sawubona', english_translation='Hello', part_of_speech='greeting')
        self.w2 = ZuluWord.objects.create(zulu_word='Hamba kahle', english_translation='Go well', part_of_speech='farewell')

    def test_increment_pair_frequency_creates_then_increments(self):
        WordPair.increment_pair_frequency(self.w1, self.w2)
        pair = WordPair.objects.get()
        self.assertEqual(pair.frequency, 1)

        # Order reversed on purpose: the model normalises pair ordering by id.
        WordPair.increment_pair_frequency(self.w2, self.w1)
        pair.refresh_from_db()
        self.assertEqual(pair.frequency, 2)
        self.assertEqual(WordPair.objects.count(), 1)  # no duplicate pair created


class UserSearchHistoryModelTests(TestCase):
    def test_history_orders_newest_first(self):
        user = User.objects.create_user('vuko', password='pass12345')
        older = UserSearchHistory.objects.create(user=user, search_query='hamba kahle')
        newer = UserSearchHistory.objects.create(user=user, search_query='sawubona')
        ordered = list(UserSearchHistory.objects.filter(user=user))
        self.assertEqual(ordered, [newer, older])


class UserFavouriteModelTests(TestCase):
    def test_a_user_cannot_favourite_the_same_word_twice(self):
        user = User.objects.create_user('vuko', password='pass12345')
        word = ZuluWord.objects.create(zulu_word='Ubuntu', english_translation='Humanity', part_of_speech='noun')
        UserFavourite.objects.create(user=user, word=word)
        with self.assertRaises(Exception):
            UserFavourite.objects.create(user=user, word=word)
