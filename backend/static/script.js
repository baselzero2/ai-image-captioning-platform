// ننتظر تحميل الصفحة بالكامل لتجنب أي فلاش أو تضارب
window.addEventListener("load", function () {

    const input = document.querySelector('input[name="image"]');
    const form = document.getElementById("captionForm");
    const preview = document.getElementById("previewImage");

    // معاينة الصورة عند اختيارها
    input.addEventListener("change", function () {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            preview.src = "";
        }
    });

    // تحميل صورة تجريبية
    window.loadSampleImage = function () {
        input.value = "";
        preview.src = "/static/uploads/sample.jpg";
    };

    // إظهار مؤشر التحميل عند إرسال النموذج
    form.addEventListener("submit", function () {
        const loading = document.getElementById("loading");
        if (loading) loading.style.display = "block";
    });
});


// رسم دائري: توزيع اللغة (لا علاقة له بالهوم)
const langCanvas = document.getElementById('languageChart');
if (langCanvas) {
    const langCtx = langCanvas.getContext('2d');
    new Chart(langCtx, {
        type: 'pie',
        data: {
            labels: ['إنجليزي', 'عربي'],
            datasets: [{
                data: [70, 30],
                backgroundColor: ['#0078d4', '#00b294']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'توزيع اللغة في الكابشنات'
                }
            }
        }
    });
}


// وظائف الصوت والنسخ
function speakCaption() {
    const caption = document.getElementById("captionText");
    if (!caption) return;

    const utterance = new SpeechSynthesisUtterance(caption.textContent);
    utterance.lang = "en-US";
    utterance.rate = 1;
    speechSynthesis.speak(utterance);
}

function stopCaption() {
    speechSynthesis.cancel();
}

function copyCaption() {
    const caption = document.getElementById("captionText");
    if (!caption) return;

    navigator.clipboard.writeText(caption.textContent)
        .then(() => {
            alert("Caption copied to clipboard!");
        })
        .catch(err => {
            console.error("Failed to copy caption:", err);
        });
}

function showArabicTranslation() {
    const div = document.getElementById("arabic-translation");
    if (div) {
        div.style.display = "block";
    }
}
