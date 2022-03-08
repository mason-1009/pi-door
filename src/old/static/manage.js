var password = null;
var auth = false;

var httpObject = new XMLHttpRequest();
var urlbase = document.location.origin;

function setContentBlur(enabled) {
    var content = document.getElementById("content-flexbox");
    if(enabled) {
        content.style.filter="blur(5px)";
    } else {
        content.style.filter="none";
    }
}

function toggleInfoPanelVisibility() {
    var panelObjects = document.getElementsByClassName("info-content-box");
    // iterate through panel objects
    for(var i=0;i<panelObjects.length;i++) {
        if(panelObjects[i].style.display=="none") {
            panelObjects[i].style.display="block";
        } else {
            panelObjects[i].style.display="none";
        }
    }
}

function setPasswordFieldOpen(enabled) {
    var object = document.getElementById("password-area");
    if(enabled) {
        object.style.display="block";
    } else {
        object.style.display="none";
    }
}

function setMessageFieldOpen(enabled) {
    var object = document.getElementById("message-area");
    if(enabled) {
        object.style.display="block";
    } else {
        object.style.display="none";
    }
}

function openPasswordPrompt() {
    // blur background
    setContentBlur(true);
    setPasswordFieldOpen(true);
}

function passwordSubmit() {
    // reset prompt state
    setPasswordFieldOpen(false);
    setContentBlur(false);
    password = document.getElementById("passfield").value;
}

function openMessagePrompt() {
    // blur background
    setContentBlur(true);
    setMessageFieldOpen(true);
}

function messageSubmit() {
    // reset prompt state
    setMessageFieldOpen(false);
    setContentBlur(false);
}

function writeDoorStatus(doorStatus, lockStatus) {
    if(doorStatus != "error") {
        document.getElementById("info-door").innerHTML=(doorStatus ? "closed":"open");
    }

    if(lockStatus != "error") {
        document.getElementById("info-lock").innerHTML=lockStatusString;
}

function writeTempStatus(temperatureString) {
    document.getElementById("info-temp").innerHTML=temperatureString;
}

// set RESTFUL API data processing function
httpObject.onreadystatechange = function() {
    var parsedResponse = null;

    if(this.readyState == 4 && this.status == 200) {
        parsedResponse = JSON.parse(httpObject.responseText);

        // check auth
        if(parsedResponse["auth"] != null && auth == false) {
            if(parsedResponse["auth"] == "success") {
                auth = true;
            } else {
                auth = false;
            }
        }
        
        if(parsedResponse["room-temperature"] != null) {
            writeTempStatus(parsedResponse["room-temperature"]);
        }

        if(parsedResponse["light-status"] != null) {
        }

        if((parsedResponse["door-status"] != null) && (parsedResponse["lock-status"] != null)) {
            writeDoorStatus(parsedResponse["door-status"],parsedResponse["lock-status"]);
        }
    }
}

function assembleURL(origin, locator, https) {
    if(https) {
        return "https://"+origin+locator;
    } else {
        return "http://"+origin+locator;
    }
}

function sendUnlockSignal() {
    if(auth) {
        httpObject.open("POST",assembleURL(urlbase,"/api/unlock",false),true,"admin",password);
        httpObject.send();
    } else {
        alert("You have not been authenticated");
    }
}

function sendLockSignal() {
    if(auth) {
        httpObject.open("POST",assembleURL(urlbase,"/api/lock",false),true,"admin",password);
        httpObject.send();
    } else {
        alert("You have not been authenticated");
    }
}

function sendMessageContent(messageText) {
    if(auth) {
        httpObject.open("POST",assembleURL(urlbase,"/api/setmotd",false),true,"admin",password);
        httpObject.send(messageText);
    } else {
        alert("You have not been authenticated");
    }
}

function resetMessage() {
    sendMessageContent("Message has not been set");
}

function fetchData() {

    if(auth == false) {
        openPasswordPrompt();
    }
        
    // grab essential data through GET requests
    httpObject.open("GET",assembleURL(urlbase,"/json/door",false), true);
    httpObject.send();

    httpObject.open("GET",assembleURL(urlbase,"/json/motd",false), true);
    httpObject.send();

    httpObject.open("GET",assembleURL(urlbase,"/json/light",false), true);
    httpObject.send();

    httpObject.open("GET",assembleURL(urlbase,"/json/temp",false), true);
    httpObject.send();

    if(auth == false) {
        httpObject.open("POST",assembleURL(urlbase,"/api/authtest",false), true);
        httpObject.send();
    }
}

window.setInterval(fetchData, 1000);
