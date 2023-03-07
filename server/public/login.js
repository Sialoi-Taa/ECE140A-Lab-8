document.addEventListener("DOMContentLoaded", () => {

    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Define the 'request' function to handle interactions with the server
    function server_request(url, data = {}, verb, callback) {
        return fetch(url, {
            credentials: 'same-origin',
            method: verb,
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(response => {
                if (callback)
                    callback(response);
            })
            .catch(error => console.error('Error:', error));
    }

    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // References to frequently accessed elements
    let form = document.getElementById('login-form');

    //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    // Handle POST Requests
    form.addEventListener('submit', (event) => {
        // Stop the default form behavior
        event.preventDefault();

        // Submit POST request to validate login entry
        /*
            1. Grab the data from the input fields
            2. Grab the action and method attributes from the form
            3. Submit a server POST request and when the server responds...
            4. Remove the alert below this comment block
        */
        // Step 1
        Username = form.elements.uname.value; // Username value
        Password = form.elements.psw.value; // Password value
        Data = {"uname":Username, "psw":Password};

        // Step 2
        Method = form.method; // POST
        Action = form.action; // http://localhost:8000/validate

        // Step 3
        server_request(Action, Data, Method, callback());

        alert('Feature is complete!');

    });

});