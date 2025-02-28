// Path: your-javascript-file.js

// Function to fetch data and populate the form
async function fetchAndPopulateInterfaces() {
    try {
        // Fetch the data from the API
        const storedData = localStorage.getItem('routerData');
        console.log("hello stored data")
        console.log(storedData);
        if (!storedData) {
            console.error('No data found in localStorage.');
            //storedData = await fetch(routersApiUrl);
        return;
        }

        const data = JSON.parse(storedData);

        // Get the router ID from the hidden input
        const routerId = document.querySelector('input[name="router"]').value;

        // Find the router with the matching ID
        const selectedRouter = data.find(router => router.id === routerId);

        if (!selectedRouter) {
            console.error('Router not found.');
            return;
        }

        // Get the container for the radio buttons
        const radioContainer = document.getElementById('interface-radio-container');

        // Clear any existing content
        radioContainer.innerHTML = '';

        // Loop through the interfaces and create radio buttons
        selectedRouter.interfaces.forEach(interface => {
            // Create a radio button for the interface
            const radioButton = document.createElement('input');
            radioButton.type = 'radio';
            radioButton.name = 'interface';
            radioButton.value = interface.name; // Use interface name as the value
            radioButton.id = `interface-${interface.name}`;

            // Create a label for the radio button
            const label = document.createElement('label');
            label.htmlFor = `interface-${interface.name}`;
            label.textContent = `${interface.name}`;

            // Append the radio button and label to the container
            radioContainer.appendChild(radioButton);
            radioContainer.appendChild(label);
            radioContainer.appendChild(document.createElement('br')); // Add a line break
        });
    } catch (error) {
        console.error('Error fetching or populating data:', error);
    }
}
// Call the function when the page loads
//document.addEventListener('DOMContentLoaded', fetchRouters);
document.addEventListener('DOMContentLoaded', () => {
    fetchAndPopulateInterfaces();
    setInterval(fetchAndPopulateInterfaces, 600000);  // Refresh every 600,000 milliseconds (10 minutes)
});
