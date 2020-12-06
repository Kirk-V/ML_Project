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
let file_size = null;
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
    
    video.addEventListener("timeupdate", stop_video);

    video.addEventListener("click", function(){
	if (this.paused == true) {
            video.play();
        }
        else{
            video.pause();
        }
    });
}

function stop_video() {
    if(this.currentTime > stop_time) {
	this.pause();
	this.currentTime = start_time;
	this.play();
    }
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
    file_size = file.size;
    
    if(file_type === null) {
	console.log("unsupported file type")
	return -1;
    }

    if(file_type === "video") {
	video.style.display = "block";
	image.style.display = "none";
	let blob = URL.createObjectURL(file)
	video.setAttribute("src", blob);
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

function send_request(that) {
    send_json(that);
    send_data(that);
}

function send_json(that) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.open("POST", "/post/send_json", true);
    httpRequest.setRequestHeader("Content-Type", "application/json");
    httpRequest.responseType = 'text';
        
    httpRequest.onreadystatechange = function() {
	if(httpRequest.readyState === 4 && httpRequest.status === 200) {
	    console.log("send_json() successful");
	}
    };
    
    let body = new Object();
    body.start = start_time;
    body.end = stop_time;
    body.file_type = file.type;
    
    httpRequest.send(JSON.stringify(body));
}

function send_data(that) {
    let httpRequest = new XMLHttpRequest();
    httpRequest.open("POST", "/post/send_data", true);
    httpRequest.setRequestHeader("Content-Type", "video/mp4");
    httpRequest.responseType = "text";
    
    httpRequest.onreadystatechange = function() {
	if(httpRequest.readyState === 4 && httpRequest.status === 200) {
	    console.log("send_data() successful")
	    make_table(JSON.parse(this.responseText));
	    get_data();
	}
    };
    
    httpRequest.send(file);
}

function get_data() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.open("POST", "/post/get_data", true);
    httpRequest.setRequestHeader("Content-Type", "video/mp4");
    httpRequest.responseType = "blob";
    
    httpRequest.onreadystatechange = function() {
	if(httpRequest.readyState === 4 && httpRequest.status === 200) {
	    console.log("get_data() successful");
	    
	    const video = document.getElementById("output_video");
	    let annotated_file = httpRequest.response
	    let blob = new Blob([annotated_file], {type: "video/mp4"});
	    
	    video.setAttribute("src", URL.createObjectURL(blob));
	    
	    video.addEventListener("timeupdate", stop_video);
	    video.addEventListener("click", function(){
		if (this.paused == true) {
		    video.play();
		}
		else{
		    video.pause();
		}
	    });
	}
    };
    
    httpRequest.send();
}

function make_table(json) {
    console.log(json);
    
    const table = document.getElementById("output_table");
    while(table.firstChild) {
	table.firstChild.remove();
    }
    
    let body = document.createElement('table');
    
    let tr = document.createElement("tr");
    for(let i=0; i < Object.keys(json.results[0]).length; i++) {
	let th = document.createElement("th");
	th.appendChild(document.createTextNode(Object.keys(json.results[0])[i]));
	tr.appendChild(th);
    }
    body.appendChild(tr);
    
    for(let i=0; i < json.results.length; i++) {
	let tr = document.createElement("tr");
	for(let j=0; j < Object.keys(json.results[i]).length; j++) {
	    let td = document.createElement("td");
	    keys = Object.keys(json.results[i]);
	    td.appendChild(document.createTextNode(json.results[i][keys[j]]));
	    tr.appendChild(td);
	}
	body.appendChild(tr);
    }
    table.appendChild(body);
}

function main() {
    return 0;
}

window.addEventListener("DOMContentLoaded", (event) => {
    main();
});
