

function draw_chart(nms,evs) {

    var ctx = document.getElementById("myChart");

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: nms,
            datasets: [{
                label: '# of Events',
                data: evs,
                backgroundColor: [
                    "#f1eef6",
                    "#f1eef6",
                    "#f1eef6",
                    "#f1eef6",
                    "#d0d1e6",
                    "#045a8d",
                    "#045a8d",
                    "#045a8d",
                    "#f1eef6",
                    ],
                borderWidth: 1
            }]
        },
      maintainAspectRatio: false,
      showTooltips: false,

      options: {responsive: true,
                maintainAspectRatio: false,
                animation: false,



          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero:true
                  }
              }]
          }
      }
  });    
} 
