# translator/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import io
import base64

translator = Translator()

class TranslateTextView(APIView):
    def post(self, request):
        text = request.data.get('text')
        target_lang = request.data.get('target_lang', 'en')
        translated = translator.translate(text, dest=target_lang)
        return Response({'translated_text': translated.text}, status=status.HTTP_200_OK)

class DetectLanguageView(APIView):
    def post(self, request):
        text = request.data.get('text')
        detected = translator.detect(text)
        return Response({'language': detected.lang}, status=status.HTTP_200_OK)

class TranslateAudioView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        target_lang = request.data.get('target_lang', 'en')

        recognizer = sr.Recognizer()
        audio_data = sr.AudioFile(file)
        with audio_data as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)

        translated = translator.translate(text, dest=target_lang)
        tts = gTTS(text=translated.text, lang=target_lang)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        # Convert audio buffer to base64 for response
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')

        return Response({
            'translated_text': translated.text,
            'audio': audio_base64
        }, status=status.HTTP_200_OK)
