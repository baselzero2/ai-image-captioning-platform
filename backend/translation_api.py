from argostranslate import translate

def translate_to_arabic(text):
    try:
        languages = translate.load_installed_languages()
        from_lang = next(lang for lang in languages if lang.code == "en")
        to_lang = next(lang for lang in languages if lang.code == "ar")
        translation = from_lang.get_translation(to_lang)
        return translation.translate(text)
    except Exception as e:
        print("⚠️ Argos translation error:", e)
        return ""
