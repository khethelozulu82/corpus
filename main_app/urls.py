from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('download/', views.download_corpus_data, name='download_corpus'),
    path('favourites/', views.favourites, name='favourites'),
    path('favourites/add/<int:word_id>/', views.add_to_favourites, name='add_to_favourites'),
    path('history/', views.history, name='history'),
    path('history/remove/<int:entry_id>/', views.remove_history_entry, name='remove_history_entry'),
    path('history/clear-all/', views.clear_all_history, name='clear_all_history'),
    path('trends/', views.trends, name='trends'),
    path('cultural_stories/', views.cultural_stories, name='cultural_stories'),
    path('help/', views.help_page, name='help'),
    path('profile/', views.profile, name='profile'),
    path('word/<int:word_id>/', views.word_detail, name='word_detail'),
]
