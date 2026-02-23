import os
import sys
import json
from flask import Flask, jsonify, request, render_template, url_for, session, redirect
from werkzeug.utils import secure_filename
from transformers.utils import logging
from translation_api import translate_to_arabic

from models import init_db
init_db()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

from routes import dashboard_bp
app.register_blueprint(dashboard_bp)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai_model')))
from caption_generator import generate_caption

from transformers.utils import logging
logging.set_verbosity_error()

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
DATA_FILE = os.path.join(BASE_DIR, 'captions_data.json')
TRANSLATION_FILE = os.path.join(BASE_DIR, 'static', 'translations.json')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.template_folder = os.path.join(BASE_DIR, 'templates')

with open(TRANSLATION_FILE, 'r', encoding='utf-8') as f:
    TRANSLATIONS = json.load(f)

model = None
processor = None

@app.before_request
def set_default_language():
    if 'lang' not in session:
        session['lang'] = 'en'

def _(text):
    lang = session.get('lang', 'en')
    return TRANSLATIONS.get(lang, {}).get(text, text)

app.jinja_env.globals.update(_=_)

@app.route('/toggle-lang', methods=['GET', 'POST'])
def toggle_lang():
    session['lang'] = 'ar' if session.get('lang', 'en') == 'en' else 'en'
    referrer = request.referrer or '/'
    if '/upload' in referrer:
        return redirect(url_for('home'))
    elif '/impact-upload' in referrer:
        return redirect(url_for('impact'))
    else:
        return redirect(referrer)

def remove_repetition(text):
    seen = set()
    result = []
    for word in text.split():
        lower_word = word.lower().strip(",.")
        if lower_word not in seen:
            seen.add(lower_word)
            result.append(word)
    return ' '.join(result)

@app.route('/')
def home():
    images = session.get('images', [])

    image_labels = [img['url'] for img in images]
    caption_lengths = [len(img['caption'].split()) if img.get('caption') else 0 for img in images]

    if images:
        last = images[-1]
        image_url = last['url']
        caption = last['caption']
        has_face = last.get('has_face', 0)
        language = last.get('language', 'Other')
        model_used = last.get('model_used', None)   # ✔ صحيح
    else:
        image_url = None
        caption = None
        has_face = 0
        language = 'Other'
        model_used = None   # ✔ مهم جدًا

    return render_template(
        'index.html',
        caption_lengths=caption_lengths,
        image_labels=image_labels,
        image_url=image_url,
        caption=caption,
        translated_caption=session.get('translated_caption'),
        has_face=has_face,
        language=language,
        model_used=model_used,  
        error=None
    )


@app.route('/upload', methods=['POST'])
def upload_image():
    global model, processor

    # 🔹 قراءة اختيار النموذج من الفورم
    model_choice = request.form.get('model_choice', 'base')

    # 🔹 تحديد مسار النموذج حسب الاختيار
    if model_choice == "base":
        local_model_path = os.path.join(BASE_DIR, 'local_model')
    else:
        local_model_path = os.path.join(BASE_DIR, '..', 'local_model_large')

    # 🔹 تحميل النموذج المختار
    from transformers import BlipProcessor, BlipForConditionalGeneration
    try:
        processor = BlipProcessor.from_pretrained(local_model_path, use_fast=True)
        model = BlipForConditionalGeneration.from_pretrained(local_model_path)
        print(f"✅ Loaded model: {model_choice} from {local_model_path}")
    except Exception as e:
        print("❌ Error loading model or processor:", e)
        return render_template(
            'index.html',
            error=_("Model loading failed. Check console for details."),
            model_used=model_choice
        )

    # 🔹 معالجة الصورة
    image = request.files.get('image')
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)
        print("📸 Image saved to:", image_path)

        try:
            caption = generate_caption(image_path, processor, model)
            caption = remove_repetition(caption)
            print("📝 Generated caption:", caption)

            # 🔹 ترجمة الكابشن إلى العربية
            translated_caption = translate_to_arabic(caption)
            session['translated_caption'] = translated_caption

            print("🌍 Arabic translation:", translated_caption)


            # 🔹 قراءة البيانات القديمة (JSON يبقى كما هو)
            data = []
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, 'r') as f:
                        content = f.read().strip()
                        if content:
                            data = json.loads(content)
                except Exception as e:
                    print("⚠️ Error reading data file:", e)

            # 🔹 إضافة بيانات جديدة إلى JSON
            data.append({
                "filename": filename,
                "length": len(caption.split())
            })

            with open(DATA_FILE, 'w') as f:
                json.dump(data, f)

            caption_lengths = [item['length'] for item in data]
            image_labels = [item['filename'] for item in data]
            image_url = url_for('static', filename=f'uploads/{filename}')

            # 🔹 تخزين آخر نتيجة في السيشن
            session['last_image_path'] = image_path
            session['last_image_url'] = image_url
            session['last_caption'] = caption

            #  إضافة الصورة إلى session['images'] (المصدر الأساسي للهوم والمودل)
            images = session.get('images', [])
            images.append({
                'url': image_url,
                'caption': caption,
                'has_face': 0,
                'language': session.get('lang', 'en'),
                'model_used': model_choice,
                'created_at': ''
            })
            session['images'] = images
            

            return render_template(
                'index.html',
                image_url=image_url,
                caption=caption,
                translated_caption=translated_caption,
                caption_lengths=caption_lengths,
                image_labels=image_labels,
                model_used=model_choice,
                error=None
            )

        except Exception as e:
            print("❌ Error generating caption:", e)
            return render_template(
                'index.html',
                error=_("Caption generation failed. Check console for details."),
                model_used=model_choice
            )

    return render_template(
        'index.html',
        error=_("No image was uploaded."),
        model_used=model_choice
    )


@app.route('/impact-upload', methods=['POST'])
def impact_upload():
    global model, processor

    if model is None or processor is None:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        try:
            local_model_path = os.path.join(BASE_DIR, 'local_model')
            processor = BlipProcessor.from_pretrained(local_model_path, use_fast=True)
            model = BlipForConditionalGeneration.from_pretrained(local_model_path)
            print("✅ Model and processor loaded successfully from:", local_model_path)
        except Exception as e:
            print("❌ Error loading model or processor:", e)
            return render_template('impact.html', error=_("Model loading failed. Check console for details."))

    image = request.files.get('image')
    if image:
        try:
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            print("📸 Image saved to:", image_path)

            caption = generate_caption(image_path, processor, model)
            caption = remove_repetition(caption)

            image_url = url_for('static', filename=f'uploads/{filename}')

            # تخزين المسار الفعلي والـ URL في السيشن
            session['last_image_path'] = image_path
            session['last_image_url'] = image_url
            session['last_caption'] = caption

            return render_template('impact.html', image_url=image_url, caption=caption)
        except Exception as e:
            print("❌ Error generating caption in impact:", e)
            return render_template('impact.html', error=_("Caption generation failed. Check console for details."))

    return render_template('impact.html', error=_("No image was uploaded."))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/impact')
def impact():
    return render_template('impact.html')

@app.route('/model')
def model_overview():
    images = session.get('images', [])

    image_labels = [img['url'] for img in images]
    caption_lengths = [len(img['caption'].split()) if img.get('caption') else 0 for img in images]

    quality_counts = {"Short": 0, "Medium": 0, "Long": 0}
    for img in images:
        if img.get('caption'):
            words = len(img['caption'].split())
            if words <= 3:
                quality_counts["Short"] += 1
            elif words <= 7:
                quality_counts["Medium"] += 1
            else:
                quality_counts["Long"] += 1

    type_counts = {}
    for img in images:
        ext = os.path.splitext(img['url'])[1].lower().replace('.', '')
        type_counts[ext] = type_counts.get(ext, 0) + 1

    return render_template(
        'model.html',
        caption_lengths=caption_lengths,
        image_labels=image_labels,
        quality_counts=quality_counts,
        type_counts=type_counts,
        total_images=len(images)
    )


@app.route('/reset', methods=['GET'])
def reset_data():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
        print("🧹 Caption data cleared successfully.")
    except Exception as e:
        print("⚠️ Error clearing file:", e)

    session.pop('last_image_path', None)
    session.pop('last_image_url', None)
    session.pop('last_caption', None)
    session.pop('images', None)


    return render_template(
        'index.html',
        caption_lengths=[],
        image_labels=[],
        image_url=None,
        caption=None,
        error=None
    )


if __name__ == '__main__':
    app.run(debug=False)
