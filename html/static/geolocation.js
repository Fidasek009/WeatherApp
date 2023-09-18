function getLocation() {
    if(navigator.geolocation) navigator.geolocation.getCurrentPosition(showPosition)
    else console.log("Geolocation not supported")
}

function showPosition(position) {
    location.href = `/?lat=${position.coords.latitude}&lon=${position.coords.longitude}`;
}

getLocation()