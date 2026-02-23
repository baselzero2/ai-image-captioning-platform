from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# تحميل النموذج الجديد
processor = BlipProcessor.from_pretrained("local_model_large")
model = BlipForConditionalGeneration.from_pretrained("local_model_large")

#  مسار صورة للاختبار
image_path = "C:/Users/ASUS/Desktop/New Images/Image 8.png" 
image = Image.open(image_path)

inputs = processor(image, return_tensors="pt")
output = model.generate(**inputs)
caption = processor.decode(output[0], skip_special_tokens=True)

print("Caption:", caption)
