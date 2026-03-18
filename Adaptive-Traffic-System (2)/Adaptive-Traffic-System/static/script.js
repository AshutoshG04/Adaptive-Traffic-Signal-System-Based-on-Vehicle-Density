// Path: static/script.js

function updateDashboard() {

    fetch("/traffic_data")
        .then(res => res.json())
        .then(data => {

            const active = data.active_lane;

            document.getElementById("activeLaneText").innerText =
                "Active Lane: " + (active + 1);

            document.getElementById("timerText").innerText =
                "Green Duration: " + data.remaining + " sec";

            document.getElementById("queueData").innerText =
                "Queue Lengths: " + data.queues.join(" | ");

            document.getElementById("densityData").innerText =
                "System Density: " + data.density;

            for (let i = 1; i <= 4; i++) {
                document.getElementById("lane" + i + "Light")
                    .classList.remove("green");
            }

            document.getElementById("lane" + (active + 1) + "Light")
                .classList.add("green");
        });
}

function overrideSignal(lane) {
    fetch("/override/" + lane);
}

setInterval(updateDashboard, 1000);
updateDashboard();