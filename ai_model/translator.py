from transformers import pipeline

# تحميل النموذج مرة واحدة فقط
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar")

def translate_caption(text):
    cleaned = text.strip()

    # إعادة صياغة الجملة لإعطاء سياق يساعد النموذج على الفهم
    contextualized = f"This is a description of an image: {cleaned}"

    # ترجمة الجملة المعاد صياغتها
    result = translator(contextualized, max_length=100)
    translated = result[0]['translation_text']

    # إزالة المقدمة الإنجليزية من الترجمة الناتجة إن وجدت
    if translated.startswith("هذا وصف لصورة:"):
        translated = translated.replace("هذا وصف لصورة:", "").strip()

    return translated
