let lengthChartInstance;
let qualityChartInstance;
let typeChartInstance;

//  Caption Length Comparison
function renderCaptionChart(imageLabels, captionLengths) {
  try {
    const lengthCanvas = document.getElementById('captionChart');
    if (lengthCanvas && Array.isArray(captionLengths) && captionLengths.length > 0) {
      if (lengthChartInstance) lengthChartInstance.destroy();
      lengthChartInstance = new Chart(lengthCanvas.getContext('2d'), {
        type: 'bar',
        data: {
          labels: imageLabels,
          datasets: [{
            label: 'Caption Length (words)',
            data: captionLengths,
            backgroundColor: ['#0078d4', '#00b294', '#ff8c00', '#e81123', '#6b69d6'],
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: { display: true, text: 'Caption Length Comparison', font: { size: 18 } },
            legend: { display: false }
          },
          scales: {
    y: { 
        beginAtZero: true, 
        ticks: { stepSize: 1 }, 
        title: { display: true, text: 'Words' } 
    },
    x: { 
        title: { display: true, text: 'Images' },
        ticks: {
            autoSkip: true,
            maxTicksLimit: 5,
            maxRotation: 0,
            minRotation: 0,
            font: { size: 11 },
            callback: function (value) {
                const label = this.getLabelForValue(value);
                return label.split('/').pop();
            }
        }
    }
}

        }
      });
    }
  } catch (e) {
    console.log("⚠️ Caption Length chart skipped:", e);
  }
}

//  Caption Quality Analysis
function renderQualityChart(qualityCounts) {
  try {
    const qualityCanvas = document.getElementById('qualityChart');
    if (qualityCanvas && qualityCounts && Object.keys(qualityCounts).length > 0) {
      if (qualityChartInstance) qualityChartInstance.destroy();
      const labels = Object.keys(qualityCounts);
      const values = Object.values(qualityCounts);

      qualityChartInstance = new Chart(qualityCanvas.getContext('2d'), {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: ['#198754', '#0d6efd', '#ffc107']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: { display: true, text: 'Caption Quality Analysis', font: { size: 18 } },
            legend: { position: 'bottom' }
          }
        }
      });
    }
  } catch (e) {
    console.log("⚠️ Quality chart skipped:", e);
  }
}

//  Image Type Distribution
function renderImageTypeChart(typeCounts) {
  try {
    const typeCanvas = document.getElementById('imageTypeChart');
    if (typeCanvas && typeCounts && Object.keys(typeCounts).length > 0) {
      if (typeChartInstance) typeChartInstance.destroy();
      const labels = Object.keys(typeCounts);
      const values = Object.values(typeCounts);

      typeChartInstance = new Chart(typeCanvas.getContext('2d'), {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: ['#6f42c1', '#20c997', '#fd7e14', '#dc3545']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: { display: true, text: 'Image Type Distribution', font: { size: 18 } },
            legend: { position: 'bottom' }
          }
        }
      });
    }
  } catch (e) {
    console.log("⚠️ Type chart skipped:", e);
  }
}
