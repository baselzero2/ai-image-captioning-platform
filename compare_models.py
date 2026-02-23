from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# تحميل النموذج الأول (Base)
processor_base = BlipProcessor.from_pretrained("backend/local_model")
model_base = BlipForConditionalGeneration.from_pretrained("backend/local_model")

# تحميل النموذج الثاني (Large)
processor_large = BlipProcessor.from_pretrained("local_model_large")
model_large = BlipForConditionalGeneration.from_pretrained("local_model_large")

print("Both models loaded successfully.")

def generate_captions(image_path):
    image = Image.open(image_path)

    # وصف النموذج الأول
    inputs_base = processor_base(image, return_tensors="pt")
    output_base = model_base.generate(**inputs_base)
    caption_base = processor_base.decode(output_base[0], skip_special_tokens=True)

    # وصف النموذج الثاني
    inputs_large = processor_large(image, return_tensors="pt")
    output_large = model_large.generate(**inputs_large)
    caption_large = processor_large.decode(output_large[0], skip_special_tokens=True)

    return {
        "base_caption": caption_base,
        "large_caption": caption_large
    }

if __name__ == "__main__":
    image_path = "C:/Users/ASUS/Desktop/New Images/Image 5.jpg"
  #مسار أي صورة  
    results = generate_captions(image_path)

    print("\n--- Comparison Result ---")
    print("Base Model Caption : ", results["base_caption"])
    print("Large Model Caption:", results["large_caption"])
