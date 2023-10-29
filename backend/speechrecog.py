import speech_recognition as sr
from googletrans import Translator


recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something:")
    audio = recognizer.listen(source)
    transcipt = recognizer.recognize_google(audio)
try:
    print("You said: " + transcipt)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio.")
except sr.RequestError:
    print("Could not request results from Google Speech Recognition service.")


def translate_to_english(text):
    translator = Translator()
    translated = translator.translate(text, src='gu', dest='en')
    print("Translated text:", translated.text)

# Example usage with Hindi text written in English
hindi_in_english = transcipt
translate_to_english(hindi_in_english)