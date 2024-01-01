function sendLocationToServer(latitude, longitude) {
    // Prepare the data to send
    const data = {
        latitude: latitude,
        longitude: longitude
    };

    // Make a fetch request to the Flask backend
    fetch('/re', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Location sent to server:', data);
    })
    .catch(error => {
        console.error('Error sending location:', error);
    });
}

function getLocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById("location").innerHTML = "Latitude: " + latitude + "<br>Longitude: " + longitude;

            // Send location data to Flask backend
            sendLocationToServer(latitude, longitude);
            document.getElementById("status").style.display = 'block';
        }, function(error) {
            // Error handling for geolocation
        });
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}
