# translator/urls.py

from django.urls import path
from .views import TranslateTextView, DetectLanguageView, TranslateAudioView

urlpatterns = [
    path('translate/text/', TranslateTextView.as_view(), name='translate-text'),
    path('detect/language/', DetectLanguageView.as_view(), name='detect-language'),
    path('translate/audio/', TranslateAudioView.as_view(), name='translate-audio'),
]
