// contains functions for modifying DOM elements on the main page

var doorAPI = new XMLHttpRequest();
var lightAPI = new XMLHttpRequest();
var tempAPI = new XMLHttpRequest();
var messageAPI = new XMLHttpRequest();

// assign page request host URL
var hostUrl = document.location.origin;

function setHideMessage(hide) {
    if(hide || hide == null) {
        document.getElementById("message").style.display="none";
    } else {
        document.getElementById("message").style.display="inline";
    }
}

function setHideInfo(hide) {
    if(hide || hide == null) {
        document.getElementById("information").style.display="none";
    } else {
        document.getElementById("information").style.display="inline";
    }
}

function setDoorStatus(doorStatus, lockStatus) {
    if(doorStatus==null || lockStatus==null) {
        document.getElementById("proplist-lockstatus").innerHTML="error";
    } else if(doorStatus==true && lockStatus==false) {
        document.getElementById("proplist-lockstatus").innerHTML="closed but unlocked";
    } else if(doorStatus==true && lockStatus==true) {
        document.getElementById("proplist-lockstatus").innerHTML="closed and locked";
    } else if(doorStatus==false && lockStatus==true) {
        document.getElementById("proplist-lockstatus").innerHTML="error; please restart";
    } else if(doorStatus==false && lockStatus==false) {
        document.getElementById("proplist-lockstatus").innerHTML="open and unlocked";
    }
}

function setRoomTemperature(degrees) {
    if(degrees != null) {
        document.getElementById("proplist-roomtemp").innerHTML=degrees.toString()+" degrees";
    } else {
        document.getElementById("proplist-roomtemp").innerHTML="error";
    }
}

function setLightStatus(power) {
    if(power != null) {
        if(power) {
            document.getElementById("proplist-lightstatus").innerHTML="lights are on";
        } else {
            document.getElementById("proplist-lightstatus").innerHTML="lights are off";
        }
    } else {
        document.getElementById("proplist-lightstatus").innerHTML="error";
    }
}

function setMessage(motdString) {
    // log info string
    if(motdString != null) {
        document.getElementById("motd-text").innerHTML=motdString;
    } else {
        document.getElementById("motd-text").innerHTML="error";
    }
}

// *** bind functions for async requests ***

// async requests are usually fetched out of order
// because of this, each binded function is called as data is collected
// the collected data is immediately parsed and injected into the DOM

doorAPI.onreadystatechange = function() {
    // data is being reused, so it is stored
    var parsedJSON = null;
    var doorStatus = null;
    var lockStatus = null;

    if(this.readyState == 4 && this.status == 200) {
        parsedJSON=JSON.parse(this.responseText);
        doorStatus=parsedJSON["door-status"];
        lockStatus=parsedJSON["lock-status"];

        // inject API data into DOM
        setDoorStatus(doorStatus, lockStatus);
    }
};

lightAPI.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
        lightStatus=JSON.parse(this.responseText)["light-status"];
    }
};

tempAPI.onreadystatechange = function() {
    var roomTemp = null;
    if(this.readyState == 4 && this.status == 200) {
        roomTemp=JSON.parse(this.responseText)["room-temperature"];
    }
};

messageAPI.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
        setMessage(JSON.parse(this.responseText)["motd"]);
    }
};


// functions for hiding and showing page elements
function setHideForecast(hide) {
    if(hide) {
        document.getElementById("forecast").style.display="none";
    } else {
        document.getElementById("forecast").style.display="inline";
    }
}

function AJAXFetchData() {
    doorAPI.open("GET", hostUrl+"/json/door", true);
    doorAPI.send();

    lightAPI.open("GET", hostUrl+"/json/light", true);
    lightAPI.send();

    tempAPI.open("GET", hostUrl+"/json/temp", true);
    tempAPI.send();

    messageAPI.open("GET", hostUrl+"/json/motd", true);
    messageAPI.send();
}

// refresh page every 2500 milliseconds
window.setInterval(AJAXFetchData, 2500);
