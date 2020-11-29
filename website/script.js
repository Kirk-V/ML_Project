//https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
const fileTypes = [
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "video/mp4",
    "video/webm"
];

function validFileType(file) {
    return fileTypes.includes(file.type);
}

function upload_file(that) {
    const video = document.getElementById("video_container").getElementsByTagName("video")[0];

    file = that.files[0];
    
    if(validFileType(file.type)) {
	console.log("unsupported file type")
	return -1;
    }

    video.setAttribute("src", URL.createObjectURL(file));
}

function seek(start, end, event) {
    const x = event.offsetX / this.offsetWidth;

    //const value =;

    
    text = document.getElementById("start_range");
    text = document.getElementById("end_range");
}

function send_request(that) {
    var httpRequest = new XMLHttpRequest();
    var response = null;
    httpRequest.onreadystatechange = function() {
	if(httpRequest.readyState == 4 && httpRequest.status == 200) {
	    response = httpRequest.responseText;
	    callback(JSON.parse(response));
	}
    };
    
    httpRequest.open("POST", "/post/send_request", true);
    httpRequest.send();
    
    wait_request();
}

function wait_request() {
    var httpRequest = new XMLHttpRequest();
    var response = null;
    httpRequest.onreadystatechange = function() {
	if(httpRequest.readyState == 4 && httpRequest.status == 200) {
	    response = httpRequest.responseText;
	    callback(JSON.parse(response));
	}
    };
    
    httpRequest.open("GET", "/get/get_result", true);
    httpRequest.send();
}

function main() {
    start = document.getElementById("start_range");
    end = document.getElementById("end_range");
    
    start.onmousemove = function(e) {seek(start, end, event)};
    end.onmousemove = function(e) {seek(start, end, event)};
    
    return 0;
}


window.addEventListener("DOMContentLoaded", (event) => {
    main();
});
