from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
import sqlite3
from datetime import datetime
from collections import Counter
import cv2
import os

dashboard_bp = Blueprint('dashboard_bp', __name__)

DB_PATH = 'dashboard.db'

# دالة كشف الوجه
def detect_face(image_path):
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        img = cv2.imread(image_path)
        if img is None:
            return 0
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        return 1 if len(faces) > 0 else 0
    except Exception as e:
        print(f"⚠️ Face detection error: {e}")
        return 0

# حفظ بيانات الصورة بعد توليدها (لـ Advanced فقط)
def save_image_data(image_url, caption, has_face, language):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO images (image_url, caption, has_face, language, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (image_url, caption, has_face, language, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        print(f"✅ Saved to DB: {caption}, {has_face}, {language}, {image_url}")
    except Exception as e:
        print(f"⚠️ DB save error: {e}")

# استقبال البيانات بعد الضغط على Generate من صفحة Home
@dashboard_bp.route('/generate-image', methods=['POST'])
def generate_image():
    caption = request.form.get('caption')
    language = request.form.get('language', 'Other')

    image_url = session.get('last_image_url')
    image_path = session.get('last_image_path')

    # كشف الوجه
    has_face = 0
    if image_path and os.path.exists(image_path):
        has_face = detect_face(image_path)

    if caption and image_url:
        images = session.get('images', [])
        # ✅ تحقق إذا الصورة موجودة بالفعل بنفس الرابط والكابشن
        exists = any(img['url'] == image_url and img['caption'] == caption for img in images)
        if not exists:
            images.append({
                'url': image_url,
                'caption': caption,
                'has_face': has_face,
                'language': language,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            session['images'] = images


        # تحديث القيم الأخيرة للعرض النصي
        session['last_caption'] = caption
        session['has_face'] = has_face
        session['language'] = language

        # حفظ للـ Advanced (قاعدة البيانات)
        save_image_data(image_url, caption, has_face, language)

    return redirect(url_for('home'))


# صفحة Advanced Dashboard (تظل تعمل على قاعدة البيانات كما كانت)
@dashboard_bp.route('/advanced-dashboard')
def advanced_dashboard():
    return render_template('advanced_dashboard.html')

# API: إرسال بيانات الرسوم البيانية لصفحة Advanced من قاعدة البيانات
@dashboard_bp.route('/dashboard-data')
def dashboard_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT image_url, caption, has_face, language, created_at FROM images')
    rows = c.fetchall()
    conn.close()

    if not rows:
        return jsonify({
            "chartWords": {"labels": [], "values": []},
            "chartUploads": {"labels": [], "values": []},
            "chartFaces": {"labels": ["With Face", "Without Face"], "values": [0, 0]},
            "chartLanguages": {"labels": [], "values": []}
        })

    # تحليل الكلمات
    all_words = []
    for row in rows:
        if row[1]:
            all_words += row[1].lower().split()
    word_counts = Counter(all_words).most_common(5)
    chartWords = {
        "labels": [w[0] for w in word_counts],
        "values": [w[1] for w in word_counts]
    }

    # نشاط رفع الصور حسب التاريخ (اليوم فقط من created_at)
    day_counts = Counter([row[4].split(" ")[0] for row in rows if row[4]])
    sorted_days = sorted(day_counts.items())
    chartUploads = {
        "labels": [d[0] for d in sorted_days],
        "values": [d[1] for d in sorted_days]
    }

    # الصور التي تحتوي على وجوه
    face_yes = sum(1 for row in rows if row[2] == 1)
    face_no = sum(1 for row in rows if row[2] == 0)
    chartFaces = {
        "labels": ["With Face", "Without Face"],
        "values": [face_yes, face_no]
    }

    # توزيع اللغات
    lang_counts = Counter([row[3] if row[3] else "Other" for row in rows])
    chartLanguages = {
        "labels": list(lang_counts.keys()),
        "values": list(lang_counts.values())
    }

    return jsonify({
        "chartWords": chartWords,
        "chartUploads": chartUploads,
        "chartFaces": chartFaces,
        "chartLanguages": chartLanguages
    })

# زر Reset لتصفير بيانات Advanced فقط (لا يلمس الـ session لضمان بقاء رسم Home)
@dashboard_bp.route('/reset-dashboard', methods=['POST'])
def reset_dashboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM images')
    conn.commit()
    conn.close()
    print("🧹 Dashboard reset, all DB data cleared (Home session data intact).")
    return redirect(url_for('dashboard_bp.advanced_dashboard'))


@dashboard_bp.route('/model')
def model():
    images = session.get('images', [])

    image_labels = [img['url'] for img in images]
    caption_lengths = [len(img['caption'].split()) if img.get('caption') else 0 for img in images]

    # حساب جودة الكابشن
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

    # حساب نوع الصور (حسب الامتداد مثلاً)
    type_counts = {}
    for img in images:
        ext = os.path.splitext(img['url'])[1].lower()
        type_counts[ext] = type_counts.get(ext, 0) + 1

    return render_template(
        'model.html',
        image_labels=image_labels,
        caption_lengths=caption_lengths,
        quality_counts=quality_counts,
        type_counts=type_counts
    )




@dashboard_bp.route('/reset-data')
def reset_data():
    session.clear()
    return redirect(url_for('home'))



@dashboard_bp.route('/model-data')
def model_data():
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
        ext = os.path.splitext(img['url'])[1].lower()
        type_counts[ext] = type_counts.get(ext, 0) + 1

    return jsonify({
        "image_labels": image_labels,
        "caption_lengths": caption_lengths,
        "quality_counts": quality_counts,
        "type_counts": type_counts
    })



