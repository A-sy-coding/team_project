var camera_button = document.querySelector("#start-camera");
var video = document.querySelector("#video");
var stop_button = document.querySelector("#stop-camera");

var recorder;

const settings = {
    video: true,
    audio: false
}

camera_button.addEventListener('click', function(e) {
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
        console.log(stream);
        video.srcObject = stream

        recorder = new MediaRecorder(stream);
        console.log(recorder);

        recorder.start();

        const blobContainer = [];

        recorder.ondataavailable = function(e){
            console.log(e.data);
            blobContainer.push(e.data)
        }

        recorder.onerror = function(e){
            return console.log(e.error || new Error(e.name));
        }

        recorder.onstop = function(e) {
            console.log(window.URL.createObjectURL(new Blob(blobContainer)));
            var newVideo = document.createElement('video');
            newVideo.height = '400'
            newVideo.width = '600'
            newVideo.autoplay = true
            newVideo.controls = true
            newVideo.innerHTML = '<source src="${window.URL.createObjectURL(new Blob(blobContainer))}" type="video/mp4">'
            document.body.removeChild(video)
            document.body.prepend(newVideo)

        }

    });
})

stop_button.addEventListener('click', function (e) {
    video.pause();
    recorder.stop();
}) 

