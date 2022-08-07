window.onload = function(){
    const parts = [];
    let mediaRecorder;


    // 초기 세팅 -> send_button 비활성화
    // document.getElementById("send_button").disabled = true;
    document.getElementById("send_button").style.visibility = 'hidden';

    // button 클릭하면 webcam을 키고, recording 수행
    document.getElementById("button").onclick = function(){

        // button 비활성화
        // document.getElementById("button").disabled = true;
        document.getElementById("button").style.visibility = 'hidden';

        // webcam 키기
        navigator.mediaDevices.getUserMedia({video:true})
        .then(stream => {
            document.getElementById("video").srcObject = stream;

            // recorder 객체를 생성하고, 1초 주기로 recording을 수행한다. -> 1초마다 ondataavailable이 호출된다.
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start(100);
            // e는 event를 의미한다. -> event.data를 parts에 넣는다.
            mediaRecorder.ondataavailable = function(e){
                parts.push(e.data);
            }
        });

        // 12초 후에 recording과 webcam이 종료되도록 설정 --> 녹화된 영상은 10초로 저장된다.
        // var time = 12*1000;
        const time = 3*1000;
        var blob;
        setTimeout(function() {
            mediaRecorder.stop();
            blob = new Blob(parts, {
                type: "video/mp4"
            });

            // 동영상으로 변환된 url을 저장한다.
            const url = URL.createObjectURL(blob);
            console.log(url);
            
            // webcam 종료
            document.getElementById("video").srcObject.getTracks().forEach(function(track) {
                track.stop();
            });

            console.log("Webcam Stop Success!");
            
            // webcam 종료 후 send_button 활성화
            // document.getElementById("send_button").disabled = false;
            document.getElementById("send_button").style.visibility = 'visible';
        }, time);
        
        document.getElementById("send_button").onclick = function(){
            console.log("Send recording video!!");

            // send_button 비활성화
            // document.getElementById("send_button").disabled = true;
            document.getElementById("send_button").style.visibility = 'hidden';
            
            // ajax를 이용하여 django server로 영상 전송
            var form = new FormData();
            form.append('video', blob);
            // data_ajax(blob);

            $.ajax({
                type: "POST",
                url: "record_video",
                // url: "{% url 'openpose:record_video' %}",
                enctype: 'multipart/form-data',
                data: form,
                // dataType: 'json',
                
                processData: false,
                contentType: false,
                // success function의 data는 views.py파일에서 HttPResponse 받은 값이 된다.
                success: function( data ){
                    $('h2').html(data);
                }
    
            })
        }
        
    }
}

