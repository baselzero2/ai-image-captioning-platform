from transformers import BlipProcessor, BlipForConditionalGeneration

# تحميل النموذج من الإنترنت
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# حفظ النموذج والمعالج في مجلد محلي
processor.save_pretrained("./local_model")
model.save_pretrained("./local_model")

print(" النموذج والمعالج تم حفظهما في local_model بنجاح.")

