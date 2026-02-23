import os
import csv
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# ============================
# 1) مسارات النماذج
# ============================

BASE_MODEL_PATH = "../backend/local_model"          # BLIP Base
LARGE_MODEL_PATH = "../local_model_large"           # BLIP Large

# ============================
# 2) مسار الصور والنتائج
# ============================

IMAGES_DIR = "images"      # ← ضع اسم مجلد الـ 100 صورة هنا
OUTPUT_CSV = "results.csv"

# ============================
# 3) تحميل النموذجين مرة واحدة
# ============================

print("🔄 Loading BLIP Base model...")
base_processor = BlipProcessor.from_pretrained(BASE_MODEL_PATH, use_fast=True)
base_model = BlipForConditionalGeneration.from_pretrained(BASE_MODEL_PATH)

print("🔄 Loading BLIP Large model...")
large_processor = BlipProcessor.from_pretrained(LARGE_MODEL_PATH, use_fast=True)
large_model = BlipForConditionalGeneration.from_pretrained(LARGE_MODEL_PATH)

# ============================
# 4) دالة توليد الكابشن
# ============================

def generate_caption(image_path, processor, model):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    output = model.generate(**inputs, max_length=30)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption.strip()

# ============================
# 5) تجهيز ملف CSV
# ============================

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "image_name",
        "base_caption",
        "base_length",
        "large_caption",
        "large_length"
    ])

    # ============================
    # 6) المرور على كل الصور
    # ============================

    for filename in os.listdir(IMAGES_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".jfif")):
            image_path = os.path.join(IMAGES_DIR, filename)
            print(f"📸 Processing: {filename}")

            # BLIP Base
            base_caption = generate_caption(image_path, base_processor, base_model)
            base_len = len(base_caption.split())

            # BLIP Large
            large_caption = generate_caption(image_path, large_processor, large_model)
            large_len = len(large_caption.split())

            # كتابة النتائج
            writer.writerow([
                filename,
                base_caption,
                base_len,
                large_caption,
                large_len
            ])

print("\n✅ Done! Results saved in results.csv")
