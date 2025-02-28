// Path: your-javascript-file.js

// API endpoint URL
const routersApiUrl = 'http://127.0.0.1:8000/playground/api/routers/';
const switchesApiUrl = 'http://127.0.0.1:8000/playground/api/switches/';
const firewallsApiUrl = 'http://127.0.0.1:8000/playground/api/firewalls/';

// Function to fetch data and populate the table
async function fetchRouters() {
    try {
        const response = await fetch(routersApiUrl); // Call the API
        console.log(response);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json(); // Parse JSON response

        // Populate table with data
        const tableBody = document.getElementById('router-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; 
        
        const runningRoutersChecklist = document.getElementById('running-routers-checklist');
        runningRoutersChecklist.innerHTML = ''; 
        
        data.forEach(router => {
            const row = document.createElement('tr');

            // Create table cells for each router property
            const idCell = document.createElement('td');
            idCell.textContent = router.id;

            const nameCell = document.createElement('td');
            nameCell.textContent = router.name;

            const ipCell = document.createElement('td');
            ipCell.textContent = router.ip_address;

            const locationCell = document.createElement('td');
            locationCell.textContent = router.location;
            
            const statusCell = document.createElement('td');
            statusCell.textContent = router.status;
            
            // Append cells to the row
            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(ipCell);
            row.appendChild(locationCell);
            row.appendChild(statusCell);
            
            // Append row to the table body
            tableBody.appendChild(row);
            // Add stopped routers to the checklist
            if (router.status.toLowerCase() === 'running') {
                const listItem = document.createElement('li');

                // Create a checkbox for each stopped router
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'selectedRouterIPs[]';
                checkbox.value = router.ip_address;

                const label = document.createElement('label');
                label.textContent = `${router.name} (ID: ${router.id}, IP: ${router.ip_address})`;
                label.htmlFor = `router-${router.id}`;

                listItem.appendChild(checkbox);
                listItem.appendChild(label);
                runningRoutersChecklist.appendChild(listItem);
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to fetch data and populate the table
async function fetchSwitches() {
    try {
        const response = await fetch(switchesApiUrl); // Call the API
        console.log(response);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json(); // Parse JSON response

        // Populate table with data
        const tableBody = document.getElementById('switch-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; 
        
        const runningswitchesChecklist = document.getElementById('running-switches-checklist');
        runningswitchesChecklist.innerHTML = ''; 
        
        data.forEach(swtch => {
            const row = document.createElement('tr');

            // Create table cells for each router property
            const idCell = document.createElement('td');
            idCell.textContent = swtch.id;

            const nameCell = document.createElement('td');
            nameCell.textContent = swtch.name;

            const ipCell = document.createElement('td');
            ipCell.textContent = swtch.ip_address;

            const locationCell = document.createElement('td');
            locationCell.textContent = swtch.location;
            
            const statusCell = document.createElement('td');
            statusCell.textContent = swtch.status;
            
            // Append cells to the row
            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(ipCell);
            row.appendChild(locationCell);
            row.appendChild(statusCell);
            
            // Append row to the table body
            tableBody.appendChild(row);
            // Add stopped routers to the checklist
            if (swtch.status.toLowerCase() === 'running') {
                const listItem = document.createElement('li');

                // Create a checkbox for each stopped router
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'selectedSwitchIPs[]';
                checkbox.value = swtch.ip_address;

                const label = document.createElement('label');
                label.textContent = `${swtch.name} (ID: ${swtch.id}, IP: ${swtch.ip_address})`;
                label.htmlFor = `router-${swtch.id}`;

                listItem.appendChild(checkbox);
                listItem.appendChild(label);
                runningswitchesChecklist.appendChild(listItem);
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to fetch data and populate the table
async function fetchFirewalls() {
    try {
        const response = await fetch(firewallsApiUrl); // Call the API
        console.log(response);
        if (!response.ok) {
            throw new Error(`An error occurred: ${response.statusText}`);
        }
        const data = await response.json(); // Parse JSON response

        // Populate table with data
        const tableBody = document.getElementById('firewall-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; 
        
        const runningfirewallsChecklist = document.getElementById('running-firewalls-checklist');
        runningfirewallsChecklist.innerHTML = ''; 
        
        data.forEach(firewall => {
            const row = document.createElement('tr');

            // Create table cells for each router property
            const idCell = document.createElement('td');
            idCell.textContent = firewall.id;

            const nameCell = document.createElement('td');
            nameCell.textContent = firewall.name;

            const ipCell = document.createElement('td');
            ipCell.textContent = firewall.ip_address;

            const locationCell = document.createElement('td');
            locationCell.textContent = firewall.location;
            
            const statusCell = document.createElement('td');
            statusCell.textContent = firewall.status;
            
            // Append cells to the row
            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(ipCell);
            row.appendChild(locationCell);
            row.appendChild(statusCell);
            
            // Append row to the table body
            tableBody.appendChild(row);
            // Add stopped routers to the checklist
            if (firewall.status.toLowerCase() === 'running') {
                const listItem = document.createElement('li');

                // Create a checkbox for each stopped router
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'selectedfirewallIPs[]';
                checkbox.value = firewall.ip_address;

                const label = document.createElement('label');
                label.textContent = `${firewall.name} (ID: ${firewall.id}, IP: ${firewall.ip_address})`;
                label.htmlFor = `firewall-${firewall.id}`;

                listItem.appendChild(checkbox);
                listItem.appendChild(label);
                runningfirewallsChecklist.appendChild(listItem);
            }
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
// Call the function when the page loads
//document.addEventListener('DOMContentLoaded', fetchRouters);
document.addEventListener('DOMContentLoaded', () => {
    fetchRouters();  // Initial data load
    fetchSwitches();  // Initial data load
    fetchFirewalls();
    setInterval(fetchRouters, 600000);  // Refresh every 600,000 milliseconds (10 minutes)
});
