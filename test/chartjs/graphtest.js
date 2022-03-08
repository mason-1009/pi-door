var chartObject = document.getElementById("chart");

var iter = 0;

var lineChart = new Chart(chartObject, {
	type: "line",
	data: {
		gridLines: {
			display: false
		},

		datasets: [{
			label: "Wack",
			data: [],
			borderColor: "#ffffff"
		}, {
			label: "Extra Wack",
			data: [],
			borderColor: "#ffffff"
		}]
	},
	options: {
		responsive: true
	}
});

function updateChart(value1, value2) {

	iter = iter + 1;

	if(lineChart.data.datasets[0].data.length < 4) {
		lineChart.data.datasets[0].data.push(value1);
	} else {
		lineChart.data.datasets[0].data[0] = lineChart.data.datasets[0].data[1];
		lineChart.data.datasets[0].data[1] = lineChart.data.datasets[0].data[2];
		lineChart.data.datasets[0].data[2] = lineChart.data.datasets[0].data[3];
		lineChart.data.datasets[0].data[3] = value1;
	}

	if(lineChart.data.datasets[1].data.length < 4) {
		lineChart.data.datasets[1].data.push(value2);
	} else {
		lineChart.data.datasets[1].data[0] = lineChart.data.datasets[1].data[1];
		lineChart.data.datasets[1].data[1] = lineChart.data.datasets[1].data[2];
		lineChart.data.datasets[1].data[2] = lineChart.data.datasets[1].data[3];
		lineChart.data.datasets[1].data[3] = value2;
	}

	lineChart.update();
	lineChart.render();
}

function fetch() {
	updateChart(Math.cos(iter)*10, Math.sin(iter)*10);
}

window.setInterval(fetch, 1000);
