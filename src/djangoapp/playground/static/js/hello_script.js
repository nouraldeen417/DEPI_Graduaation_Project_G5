// Fetch and display devices

const apiUrl = '/playground/api/devices/';
// Function to fetch device data from the API and update the table
async function fetchDeviceData() {
    try {
        const response = await fetch(apiUrl); // Replace with the actual API endpoint
        if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
        }

        const devices = await response.json();

        // Clear existing rows in the table body
        const tableBody = document.querySelector("#deviceTable tbody");
        tableBody.innerHTML = "";

        // Populate the table with device data
        devices.forEach(device => {
            const row = document.createElement("tr");

            const hostCell = document.createElement("td");
            hostCell.textContent = device.host;
            row.appendChild(hostCell);

            const taskCell = document.createElement("td");
            taskCell.textContent = device.task;
            row.appendChild(taskCell);

            const statusCell = document.createElement("td");
            statusCell.textContent = device.status;
            row.appendChild(statusCell);

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching device data:", error);
    }
}

// Fetch data on page load and refresh every 10 minutes (600,000 milliseconds)
fetchDeviceData();
setInterval(fetchDeviceData, 600000); // 10 minutes
