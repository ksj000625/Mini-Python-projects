from googletrans import Translator, constants
from pprint import pprint
translator=Translator()
# translate a spanish text to english text (by default)
translation = translator.translate("Hola Mundo")
print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
sentences = [
    "Hello everyone",
    "How are you ?",
    "Do you speak english ?",
    "Good bye!"
]
translations = translator.translate(sentences, dest="tr")
for translation in translations:
    print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

detection = translator.detect("नमस्ते दुनिया")
print("Language code:", detection.lang)
print("Confidence:", detection.confidence)
print("Language:", constants.LANGUAGES[detection.lang])
