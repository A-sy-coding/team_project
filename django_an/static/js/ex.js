// ajax 함수
// function data_ajax(blob){
//     $.ajax({
//                 type: "POST",
//                 // openpose apllication의 urls.py파일에서 name이 record인 함수 호출
//                 // url: "{% url 'openpose:record' %}",
//                 url: "record_video",
//                 data: {
//                     'video' : blob
//                 },
//                 dataType: 'json',
//                 processData: false,
//                 contentType: false,
//             })
// };

window.onload = function(){
    const parts = [];
    let mediaRecorder;
    
    // button 클릭하면 webcam을 키고, recording 수행
    document.getElementById("button").onclick = function(){
        navigator.mediaDevices.getUserMedia({video:true})
        .then(stream => {
            document.getElementById("video").srcObject = stream;

            // recorder 객체를 생성하고, 1초 주기로 recording을 수행한다. -> 1초마다 ondataavailable이 호출된다.
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start(1000);
            // e는 event를 의미한다. -> event.data를 parts에 넣는다.
            mediaRecorder.ondataavailable = function(e){
                parts.push(e.data);
            }
        });

        // 12초 후에 recording과 webcam이 종료되도록 설정 --> 녹화된 영상은 10초로 저장된다.
        // var time = 12*1000;
        var time = 6*1000;
        setTimeout(function() {
            mediaRecorder.stop();
            const blob = new Blob(parts, {
                type: "video/mp4"
            });

            // 동영상으로 변환된 url을 저장한다.
            const url = URL.createObjectURL(blob);
            console.log(url);
            
            // webcam 종료
            document.getElementById("video").srcObject.getTracks().forEach(function(track) {
                track.stop();
            });

            // ajax를 이용하여 django server로 영상 전송
            var form = new FormData();
            form.append('video', blob);
            // data_ajax(blob);
            $.ajax({
                type: "POST",
                // openpose apllication의 urls.py파일에서 name이 record인 함수 호출
                // url: "{% url 'openpose:record' %}",
                
                url: "record_video",
                enctype: 'multipart/form-data',
                // data: {
                //     'video' : blob
                // },
                data: form,
                // dataType: 'json',
                processData: false,
                contentType: false,
            })
            console.log("POST Success!");

        }, time);
    }
}

