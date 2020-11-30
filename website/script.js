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
let video_length = null;
let file = null;
let file_type = null;

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
    const video = document.getElementById("video_container").getElementsByTagName("video")[0];
    const image = document.getElementById("video_container").getElementsByTagName("img")[0];

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
	    setup(video.duration);	
	});
    }

    if(file_type === "image") {
	video.style.display = "none";
	image.style.display = "block";
	image.setAttribute("src", URL.createObjectURL(file));
    }
}

//https://www.simple.gy/blog/range-slider-two-handles/
function seek(target, event) {
    start_range = document.getElementById("start_range");
    end_range = document.getElementById("end_range");
    
    start_time = document.getElementById("start_time");
    end_time = document.getElementById("end_time");

    let pivot = null;
    
    if(target === start_range) {
	if(start_range.valueAsNumber >= start_range.max) {
	    pivot = Math.min(video_length, Number(start_range.max) );
	}		
    }
    else if(target === end_range) {
	if(end_range.valueAsNumber <= end_range.min) {
	    pivot = Math.min(0, Number(end_range.min));
	}
    }

    if(pivot != null) {
	start_range.max = pivot;
	end_range.min = pivot;
    }
    
    start_range.style.flexGrow = Number(start_range.max) - Number(start_range.min);
    end_range.style.flexGrow = Number(end_range.max) - Number(end_range.min);

    start_time.value = start_range.value;
    end_time.value = end_range.value;
}

function setup(length) {
    video_length = length;
    start = document.getElementById("start_range");
    end = document.getElementById("end_range");

    start_time = document.getElementById("start_time");
    end_time = document.getElementById("end_time");
    
    start.min = 0;
    start.max = video_length/2;
    end.min = video_length/2;
    end.max = video_length;

    start_time.value = video_length*0.25;
    end_time.value = video_length*0.75;
}

function send_request(that) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.open("POST", "/post/send_request", true);
    httpRequest.setRequestHeader("Content-type", file.type);
    httpRequest.responseType = 'text';
        
    httpRequest.onreadystatechange = function() {
	if(httpRequest.readyState === 4 && httpRequest.status === 200) {
	    process_response(httpRequest.responseText);
	}
    };
    
    httpRequest.send(file);
    
}

function process_response(response) {
    output = document.getElementById("output");
    output.innerHTML = response;
}

function main() {
    start = document.getElementById("start_range");
    end = document.getElementById("end_range");
    
    start_range.onmousemove = function(e) {seek(start, event)};
    end_range.onmousemove = function(e) {seek(end, event)};
    
    return 0;
}

window.addEventListener("DOMContentLoaded", (event) => {
    main();
});
