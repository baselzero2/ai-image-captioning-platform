from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# تحميل النموذج الأول (Base)
processor_base = BlipProcessor.from_pretrained("backend/local_model")
model_base = BlipForConditionalGeneration.from_pretrained("backend/local_model")


# تحميل النموذج الثاني (Large)
processor_large = BlipProcessor.from_pretrained("local_model_large")
model_large = BlipForConditionalGeneration.from_pretrained("local_model_large")

print("Both models loaded successfully.")
