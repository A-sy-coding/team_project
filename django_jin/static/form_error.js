function create_error(value){
    var newDiv = document.createElement('div');
    newDiv.innerHTML = '<div>'+ value+" 오류" +'</div>';
}


var csrftoken = $('[name=csrfmiddlewaretoken]').val();
$(function(){
    $('#idbutton').click(function(){
        var id = $('#user_id').val()
        if(id == ''){
            alert('아이디를 입력해주세요.')
            return;
        }
        $.ajax({
            url:'idvalid/',
            type:'post',
            dataType:'json',
            headers: {'X-CSRFToken': csrftoken},
            data:{user_id:id},
            success:function(response){
                if(response.data == 'exist'){
                    alert("존재하는 아이디 입니다!ㅇㅠㅇ");
                    $('#user_id').val('').focus();
                    return;
                }
                else{
                    $('#idbutton').attr("disabled", true);
                    $('#user_id').attr("disabled", true);
                    alert("사용가능한 아이디입니다!");
                    return;

                }
            },
            error : function(xhr, error){
                alert("서버와의 통신에서 문제가 발생했습니다.");
                console.error("error : " + error);
            }
        })
    })
});

$(function(){
    $('#emailval').click(function(){
        var email = $('#email').val()
        if(email == ''){
            alert('이메일을 입력해주세요.');
            return;
        }
        alert("인증번호가 전송되었습니다.");
        $.ajax({
            url:'emailvalid/',
            type:'get',
            dataType:'json',
            headers: {'X-CSRFToken': csrftoken},
            data:{email:email},
            success:function(){
                document.getElementById("auth_num").setAttribute('style','display:block;');
                document.getElementById("authnum_button").setAttribute('style','display:block;');
            }
        })

    })
})

$(function(){
    $('#authnum_button').click(function(){
        var auth_num = $('#auth_num').val();
        if(auth_num == ''){
            alert('인증번호를 입력해주세요.');
            return;
        }
        $.ajax({
            url:'authnumvalid/',
            type:'post',
            dataType:'json',
            headers: {'X-CSRFToken': csrftoken},
            data:{auth_num:auth_num},
            success:function(response){
                if (response.data == 'cor'){
                $('#auth_num').attr('disabled',true);
                $('#authnum_button').attr('disabled',true);
                }
                else{alert("인증번호가 일치하지 않습니다");
                }
            },
            error : function(xhr, error){
                alert("서버와의 통신에서 문제가 발생했습니다.");
                console.error("error : " + error);
            }
        })
    })
})