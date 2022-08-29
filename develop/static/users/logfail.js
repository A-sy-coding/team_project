$.ajax({
    url:'',
    type:'post',
    dataType:'json',
    headers: {'X-CSRFToken': csrftoken},
    data:{user_id:id},
    success:function(response){
        if(response.data == 'exist'){
            alert("존재하는 아이디 입니다!ㅇㅠㅇ");
            cleaner['user_id'] = 0;
            $('#user_id').val('').focus();
            return;
        }
        else{
            $('#idbutton').attr("disabled", true);
            alert("사용가능한 아이디입니다!");
            cleaner['user_id'] = 1;
            return;
        
        }
    },
    error : function(xhr, error){
        alert("서버와의 통신에서 문제가 발생했습니다.");
        console.error("error : " + error);
    }
})