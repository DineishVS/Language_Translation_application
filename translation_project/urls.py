# translation_project/urls.py

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from translator.views import TranslateTextView, DetectLanguageView, TranslateAudioView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/translate/text/', TranslateTextView.as_view(), name='translate_text'),
    path('api/detect/language/', DetectLanguageView.as_view(), name='detect_language'),
    path('api/translate/audio/', TranslateAudioView.as_view(), name='translate_audio'),
    path('', TemplateView.as_view(template_name='index.html')),
]
