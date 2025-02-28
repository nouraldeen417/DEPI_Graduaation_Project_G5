const routersApiUrl = '/playground/api/switches/';
let currentDeviceData = null;

// Function to switch tabs
function openTab(tabName) {
    const tabcontent = document.getElementsByClassName('tabcontent');
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = 'none';
    }
    document.getElementById(tabName).style.display = 'block';

    const tablinks = document.getElementsByClassName('tablink');
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove('active');
    }
    document.querySelector(`button[onclick="openTab('${tabName}')"]`).classList.add('active');
}

// Function to enable configure button
function enableConfigureButton() {
    const configureButton = document.getElementById('configure-btn');
    configureButton.disabled = false;
}

// Function to fetch device information
async function fetchDeviceInfo() {
    try {
        const storedData = localStorage.getItem('switchData');
        //console.log("hello stored data")
        //console.log(storedData);
        if (!storedData) {
            console.error('No data found in localStorage.');
            storedData = await fetch(routersApiUrl);
        return;
        }

        const data = JSON.parse(storedData);
        console.log(data)
        const deviceSelect = document.getElementById('device-select');
        const selectedDeviceId = deviceSelect.value;
        
        // Find the selected device
        const selectedDevice = data.find(d => d.id === selectedDeviceId);
        currentDeviceData = selectedDevice;
        console.log(selectedDevice)
        if (selectedDevice) {
            // Enable configure button when device is selected
            enableConfigureButton();
            
            // Populate Interfaces Table
            const interfacesTable = document.getElementById('interfaces-table');
            interfacesTable.innerHTML = selectedDevice.interfaces.map(intf => `
                <tr>
                    <td>${intf.name}</td>
                    <td>${intf.address_subnet.length > 0 ? 
                        `${intf.address_subnet[0].address}/${intf.address_subnet[0].subnet}` : ''}</td>
                    <td class="status-${intf.status.toLowerCase()}">${intf.status}</td>
                    <td>${intf.description || ''}</td>
                </tr>
            `).join('');

            // Populate Neighbors Table
            const neighborsTable = document.getElementById('neighbors-table');
            neighborsTable.innerHTML = selectedDevice.neighbors.map(neighbor => `
                <tr>
                    <td>${neighbor.name}</td>
                    <td>${neighbor.address_subnet}</td>
                    <td>${neighbor.port}</td>
                </tr>
            `).join('');
            // Populate Routing Table
            const vlanTableBody = document.getElementById('vlan-table-body');
            if (selectedDevice.vlan) {
                vlanTableBody.innerHTML = selectedDevice.vlan.map(vl => `
                    <tr>
                        <td>${vl.id}</td>
                        <td>${vl.name}</td>
                        <td>${vl.status}</td>
                        <td>${vl.port}</td>
                    </tr>
                `).join('');
            }
        }
    } catch (error) {
        console.error('Error fetching device info:', error);
    }
}

// Function to populate device select options
async function populateDeviceSelect() {
    try {
        const response = await fetch(routersApiUrl);
        const data = await response.json();
        console.log(data);
        localStorage.setItem('switchData', JSON.stringify(data));
        const deviceSelect = document.getElementById('device-select');
        deviceSelect.innerHTML = data.map(device => 
            `<option value="${device.id}">${device.device}</option>`
        ).join('');
        
        // Fetch initial device data
        fetchDeviceInfo();
    } catch (error) {
        console.error('Error fetching devices:', error);
    }
}

// Function to handle configure button click
function handleConfigureClick() {
    if (currentDeviceData) {
        window.location.href = `/playground/switchconfiguration?switch=${encodeURIComponent(currentDeviceData.id)}`;
    } else {
        alert('Please select a device to configure.');
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    const configureButton = document.getElementById('configure-btn');
    const deviceSelect = document.getElementById('device-select');
    
    // Add event listeners
    configureButton.addEventListener('click', handleConfigureClick);
    deviceSelect.addEventListener('change', () => {
        fetchDeviceInfo();
        enableConfigureButton();
    });
    
    // Initial setup
    openTab('interfaces');
    populateDeviceSelect();
    
    // Set up auto-refresh
    setInterval(fetchDeviceInfo, 600000); // Refresh every 10 minutes
});

