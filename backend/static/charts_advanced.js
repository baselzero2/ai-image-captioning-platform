let chartWords, chartUploads, chartFaces, chartLanguages;

async function loadAdvancedCharts() {
  try {
    const response = await fetch('/dashboard-data');
    const data = await response.json();

    
//  الكلمات الأكثر تكرارًا
if (chartWords) {
  chartWords.destroy(); // ✅ أزل الرسم القديم تمامًا
}

chartWords = new Chart(document.getElementById('chartWords'), {
  type: 'bar',
  data: {
    labels: data.chartWords.labels,
    datasets: [{
      label: 'Top Caption Words',
      data: data.chartWords.values,
      backgroundColor: ['#2196f3', '#43a047', '#f9a825', '#ff6f00', '#00acc1']
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Most Frequent Words in Captions',
        color: '#ff6f00',
        font: { size: 18 }
      },
      legend: { display: false }
    }
  }
});


    //  نشاط رفع الصور حسب الأيام
    if (chartUploads) {
      chartUploads.data.labels = data.chartUploads.labels;
      chartUploads.data.datasets[0].data = data.chartUploads.values;
      chartUploads.update();
    } else {
      chartUploads = new Chart(document.getElementById('chartUploads'), {
        type: 'line',
        data: {
          labels: data.chartUploads.labels,
          datasets: [{
            label: 'Images Uploaded',
            data: data.chartUploads.values,
            borderColor: '#43a047',
            backgroundColor: 'rgba(67,160,71,0.2)',
            fill: true,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Weekly Upload Activity',
              color: '#ff6f00',
              font: { size: 18 }
            }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    }

    //  نسبة الصور التي تحتوي على وجوه
    if (chartFaces) {
      chartFaces.data.labels = data.chartFaces.labels;
      chartFaces.data.datasets[0].data = data.chartFaces.values;
      chartFaces.update();
    } else {
      chartFaces = new Chart(document.getElementById('chartFaces'), {
        type: 'doughnut',
        data: {
          labels: data.chartFaces.labels,
          datasets: [{
            data: data.chartFaces.values,
            backgroundColor: ['#f9a825', '#2196f3']
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Face Detection in Images',
              color: '#ff6f00',
              font: { size: 18 }
            }
          }
        }
      });
    }

    //  توزيع اللغات
    if (chartLanguages) {
      chartLanguages.data.labels = data.chartLanguages.labels;
      chartLanguages.data.datasets[0].data = data.chartLanguages.values;
      chartLanguages.update();
    } else {
      chartLanguages = new Chart(document.getElementById('chartLanguages'), {
        type: 'pie',
        data: {
          labels: data.chartLanguages.labels,
          datasets: [{
            data: data.chartLanguages.values,
            backgroundColor: ['#ff6f00', '#2196f3', '#43a047', '#6f42c1']
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Caption Language Distribution',
              color: '#ff6f00',
              font: { size: 18 }
            }
          }
        }
      });
    }

  } catch (err) {
    console.error("⚠️ Error loading advanced charts:", err);
  }
}

// استدعاء عند تحميل الصفحة
document.addEventListener("DOMContentLoaded", () => {
  loadAdvancedCharts();              // أول مرة عند فتح الصفحة
  setInterval(loadAdvancedCharts, 5000); // تحديث كل 5 ثواني
});

// ✅ استدعاء مباشر بعد توليد الكابشن
document.addEventListener("captionGenerated", () => {
  loadAdvancedCharts();
});
