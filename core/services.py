import deepl
import os

def translate_deepl(text, source_lang, target_lang):
    auth_key = os.getenv("DEEPL_API_KEY")
    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, source_lang=source_lang.upper(), target_lang=target_lang.upper())
        return result.text  
    except deepl.DeepLException as e:
        print(f"Error durante la traducción: {e}")
        return None