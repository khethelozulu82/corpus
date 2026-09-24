# main_app/management/commands/corpus_stats.py
from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from main_app.models import ZuluWord, UserSearchHistory, WordPair

class Command(BaseCommand):
    help = 'Generate statistics report for the isiZulu corpus'
    
    def handle(self, *args, **options):
        # Basic statistics
        total_words = ZuluWord.objects.count()
        denominator = total_words or 1  # avoid division by zero on an empty database
        words_with_cultural_context = ZuluWord.objects.filter(
            ~Q(cultural_context='')
        ).count()
        words_with_examples = ZuluWord.objects.filter(
            ~Q(example_sentence_zulu='')
        ).count()
        
        # Search statistics
        total_searches = UserSearchHistory.objects.count()
        unique_searches = UserSearchHistory.objects.values('search_query').distinct().count()
        
        # Word pair statistics
        total_word_pairs = WordPair.objects.count()
        
        # Print report
        self.stdout.write("=" * 50)
        self.stdout.write("isiZulu Cultural Corpus Statistics Report")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Total words: {total_words}")
        self.stdout.write(f"Words with cultural context: {words_with_cultural_context} ({words_with_cultural_context/denominator*100:.1f}%)")
        self.stdout.write(f"Words with examples: {words_with_examples} ({words_with_examples/denominator*100:.1f}%)")
        self.stdout.write(f"Total searches: {total_searches}")
        self.stdout.write(f"Unique search queries: {unique_searches}")
        self.stdout.write(f"Word pairs: {total_word_pairs}")
        self.stdout.write("=" * 50)
        
        # Most searched words
        self.stdout.write("\nTop 10 most searched words:")
        top_searched = ZuluWord.objects.annotate(
            search_count=Count('usersearchhistory')
        ).order_by('-search_count')[:10]
        
        for i, word in enumerate(top_searched, 1):
            self.stdout.write(f"{i}. {word.zulu_word} ({word.search_count} searches)")
        
        self.stdout.write("=" * 50)