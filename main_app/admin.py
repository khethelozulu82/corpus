from django.contrib import admin
from .models import ZuluWord, WordPair, UserSearchHistory, UserFavourite

@admin.register(ZuluWord)
class ZuluWordAdmin(admin.ModelAdmin):
    list_display = ('zulu_word', 'english_translation', 'get_part_of_speech_display', 'date_added')
    list_filter = ('part_of_speech', 'date_added')
    search_fields = ('zulu_word', 'english_translation')
    readonly_fields = ('date_added',)
    filter_horizontal = ('synonyms',)
    
    fieldsets = (
        (None, {
            'fields': ('zulu_word', 'english_translation', 'part_of_speech')
        }),
        ('Pronunciation', {
            'fields': ('pronunciation_guide',),
            'classes': ('collapse',)
        }),
        ('Context & Examples', {
            'fields': ('cultural_context', 'example_sentence_zulu', 'example_sentence_english'),
            'classes': ('collapse',)
        }),
        ('Relationships', {
            'fields': ('synonyms',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('date_added',),
            'classes': ('collapse',)
        })
    )

@admin.register(WordPair)
class WordPairAdmin(admin.ModelAdmin):
    list_display = ('get_word1', 'get_word2', 'frequency')
    list_filter = ('frequency',)
    search_fields = ('word1__zulu_word', 'word2__zulu_word')
    
    def get_word1(self, obj):
        return obj.word1.zulu_word
    get_word1.short_description = 'Word 1'
    
    def get_word2(self, obj):
        return obj.word2.zulu_word
    get_word2.short_description = 'Word 2'

@admin.register(UserSearchHistory)
class UserSearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_query', 'search_date')
    list_filter = ('search_date', 'user')
    readonly_fields = ('search_date',)
    filter_horizontal = ('search_results',)

@admin.register(UserFavourite)
class UserFavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_word', 'date_added')
    list_filter = ('date_added', 'user')
    readonly_fields = ('date_added',)
    
    def get_word(self, obj):
        return obj.word.zulu_word
    get_word.short_description = 'Word'

# Customize admin site
admin.site.site_header = 'isiZulu Cultural Corpus Administration'
admin.site.site_title = 'isiZulu Corpus Admin'
admin.site.index_title = 'Database Administration'