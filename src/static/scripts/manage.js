var httpObject = new XMLHttpRequest();

var password = null;

var doorStatus = null;
var lockStatus = null;
var autolockEnabled = null;
var lightStatus = null;
var temperature = null;
var messageContent = null;

function setDoorString(door, lock) {
    var doorElement = document.getElementById("info-door");
    var lockElement = document.getElementById("info-lock");

    if(door == true) {
        doorElement.innerHTML = "closed";
    } else if(door == false) {
        doorElement.innerHTML = "open";
    } else {
        doorElement.innerHTML = "transmission error";
    }

    if(lock == true) {
        lockElement.innerHTML = "locked";
    } else if(lock == false) {
        lockElement.innerHTML = "unlocked";
    } else {
        lockElement.innerHTML = "transmission error";
    }
}

function setAutolockString(enabled) {
    var element = document.getElementById("info-autolock");

    if(enabled) {
        element.innerHTML = "enabled";
    } else {
        element.innerHTML = "disabled";
    }
}

function sendUnlockSignal() {
    httpObject.open("POST","/unlockdoor",true);
    httpObject.send();
}

function sendLockSignal() {
    httpObject.open("POST","/lockdoor",true);
    httpObject.send();
}

function sendAutolockToggleSignal() {
    httpObject.open("POST","/toggleAutolock",true);
    httpObject.send();
}

httpObject.onreadystatechange = function() {
    
    if(this.readyState == 4 && this.status == 200) {
        
        var parsed = JSON.parse(this.responseText);

        if(parsed["door-status"] != null) {
            doorStatus = parsed["door-status"];
        } else {
            doorStatus = null;
        }

        if(parsed["lock-status"] != null) {
            lockStatus = parsed["lock-status"];
        } else {
            lockStatus = null;
        }

        if(parsed["autolock-enabled"] != null) {
            autolockEnabled = parsed["autolock-enabled"];
        } else {
            autolockEnabled = null;
        }
            
        if(parsed["motd"] != null) {
            messageContent = parsed["motd"];
        } else {
            messageContent = null;
        }

        if(parsed["light-status"] != null) {
            lightStatus = parsed["light-status"];
        } else {
            lightStatus = null;
        }

        if(parsed["temperature"] != null) {
            temperature = parsed["temperature"];
        } else {
            temperature = null;
        }

        setDoorString(doorStatus, lockStatus);
        setAutolockString(autolockEnabled);
    }
}

function fetchAJAJ() {
    httpObject.open("GET", "/infodigest", true);
    httpObject.send();
}

function toggleInfoVisibility() {
    var element = document.getElementById("main-info-box");

    if(element.style.display == "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

function setPasswordField(visible) {
    var element = document.getElementById("password-area");

    if(element.style.display == "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

function setMessageField(visible) {
    var element = document.getElementById("message-area");

    if(visible == true) {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

function submitPassword() {
    var element = document.getElementById("passfield");
    password = element.innerHTML;
    element.innerHTML = "";
    setPasswordField(false);
}

function submitMessage() {
    var element = document.getElementById("messagefield");
    httpObject.open("POST", "/setmessage", true);
    // encode POST data into urlencode form
    httpObject.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    httpObject.send("motdtext="+encodeURIComponent(element.value));
    element.value = "";
    setMessageField(false);
}

window.setInterval(fetchAJAJ, 2500);
