var lineGraph = null;

function buildGraph(canvasID) {
    
    var chartCanvasObject = document.getElementById(canvasID);
    lineGraph = new Chart(chartCanvasObject, {
        type: "line",
        data: {
            datasets: [{
                label: "Temperature",
                data: [],
                borderColor: "#f18c8e"
            }, {
                label: "Humidity",
                data: [],
                borderColor: "f1d185"
            }]
        },
        options: {
            responsive: true
        }
    });
}

function updateChart(temperature, humidity) {

    // update temperature data
    if(lineGraph.data.datasets[0].data.length < 6) {
        lineGraph.data.datasets[0].data.push(temperature);
    } else {
        for(int i=0;i<5;i++) {
            lineGraph.data.datasets[0].data[i] = lineGraph.data.datasets[0].data[i+1];
        }
        lineGraph.data.datasets[0].data[5] = temperature;
    }

    // update humidity data
    if(lineGraph.data.datasets[1].data.length < 6) {
        lineGraph.data.datasets[1].data.push(humidity);
    } else {
        for(int i=0;i<5;i++){
            lineGraph.data.datasets[1].data[i] = lineGraph.data.datasets[1].data[i+1];
        }
        lineGraph.data.datasets[1].data[5] = humidity;
    }
}
