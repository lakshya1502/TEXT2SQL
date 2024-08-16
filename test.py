from googletrans import Translator

# Initialize the Translator
translator = Translator()

# Hinglish text to be translated
text = "5 class mai kitne bachche hai"

# Translate the text from Hinglish to Hindi
translated_text = translator.translate(text, src='hi', dest='en')

# Print the original Hinglish text and its translation
print(f"Original Hinglish Text: {text}")
print(f"Translated Text: {translated_text.text}")
