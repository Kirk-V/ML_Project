//https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
const video_file_types = [
    "video/mp4",
    "video/webm"
];

const image_file_types = [
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif"
];

//in seconds
let video_length = 100;
let file = null;
let file_type = null;
let start_time = null;
let stop_time = null;

function setup() {
    //setup slider
    let slider = document.getElementById("slider");
    start_time = video_length*0.25;
    stop_time = video_length*0.75;
    noUiSlider.create(slider, {
	start: [start_time, stop_time],
	connect: true,
	range: {
            'min': 0,
            'max': Number(video_length)
	}
    });
    
    //hook it into inputs
    const start = document.getElementById("start_time");
    const end = document.getElementById("end_time");
    const video = document.getElementById("video_player");
    
    slider.noUiSlider.on('update', function (values, handle) {
	let value = values[handle];

	if (handle) {
            end.value = value;
	    stop_time = value;
	}
	else {
            start.value = Math.round(value);
	    start_time = value;
	    video.currentTime = value;
	}
    });

    start.addEventListener('change', function () {
	slider.noUiSlider.set([this.value, null]);
	start_time = this.value;
	video.currentTime = this.value;
    });

    end.addEventListener('change', function () {
	slider.noUiSlider.set([null, this.value]);
	stop_time = this.value;
    });

    //setup video
    this.currentTime = start_time;
    
    video.addEventListener("timeupdate", function(){
	if(this.currentTime > stop_time) {
            this.pause();
	    this.currentTime = start_time;
	    this.play();
	}
    });

    video.addEventListener("click", function(){
	if (this.paused == true) {
            video.play();
        }
        else{
            video.pause();
        }
    });
}

function validFileType(type) {
    if(video_file_types.includes(type)) {
	return "video";
    }
    if(image_file_types.includes(type)) {
	return "image";
    }
    return null;
}

function upload_file(that) {
    video_length = null;
    const video = document.getElementById("video_player");
    const image = document.getElementById("image_player");

    file = that.files[0];
    file_type = validFileType(file.type)
    
    if(file_type === null) {
	console.log("unsupported file type")
	return -1;
    }

    if(file_type === "video") {
	video.style.display = "block";
	image.style.display = "none";
	video.setAttribute("src", URL.createObjectURL(file));
	video.addEventListener('loadedmetadata', function() {
	    video_length = video.duration;
	    setup();
	});
    }

    if(file_type === "image") {
	video.style.display = "none";
	image.style.display = "block";
	image.setAttribute("src", URL.createObjectURL(file));
    }
}

function set_video_time(start, end) {
    const video = document.getElementById("video_player");
    video.currentTime = start;
    start_time = start;
    stop_time = end;
}

function send_request(that) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.open("POST", "/post/send_request", true);
    httpRequest.setRequestHeader("Content-type", "application/json");
    httpRequest.responseType = 'text';
        
    httpRequest.onreadystatechange = function() {
	if(httpRequest.readyState === 4 && httpRequest.status === 200) {
	    process_response(httpRequest.responseText);
	}
    };

    start = start_time;
    end = end_time;
    
    let req = new Object();
    req.start = start;
    req.end = end;
    req.file_type = file.type;

    //could find a way to actually clip the video and only send that
    //could also send two posts, one json, one binary blob instead (should be faster)
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function() {
	req.media_file = reader.result.substr(reader.result.indexOf(",")+1);
	httpRequest.send(JSON.stringify(req));
    }    
}

function process_response(response) {
    output = document.getElementById("output");
    output.innerHTML = response;
}

function main() {

    return 0;
}

window.addEventListener("DOMContentLoaded", (event) => {
    main();
});
