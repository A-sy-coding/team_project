const blank_regExp = /\s/g;
const int_regExp = /^[0-9]+$/;
const email_regExp = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;
const phone_regExp=/^\d{3}-\d{3,4}-\d{4}$/;
const pattern_regExp = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi;
const pw_regExp = /^(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$/;
var id_clean = false;
var pw_clean = false;
var pw_clean2=false;
var email_clean = false;
var sex_clean = false;
var birth_clean = false;
var name_clean = false;





function pw_valid(){
    var pw= document.getElementById('pw1').value;
    if (pw_regExp.test(pw)==false){//관련정규식 투입
            document.getElementById('pw_error').innerText='영문자,숫자,특수문자를 포함한 8자리이상의 비밀번호를 입력해주세요'}
    else{document.getElementById('pw_error').innerText='사용가능한 비밀번호입니다.';pw_clean=true}    
        }
function pw_valid2(){
    var pw1= document.getElementById('pw1').value;
    console.log(pw1)
    var pw2= document.getElementById('pw2').value;
    if (pw1==pw2){document.getElementById('pw2_error').innerText='비밀번호가 일치합니다.';pw_clean2=true;}
    else{document.getElementById('pw2_error').innerText='비밀번호가 일치하지 않습니다.';pw_clean2=false}}

var csrftoken = $('[name=csrfmiddlewaretoken]').val();
$(function(){
    $('#idbutton').click(function(){
        var id = $('#user_id').val()
        if ((new RegExp(/^[A-Za-z0-9]{6,}$/)).test(id) == false) {
            alert("ID는 6자리 이상의 영숫자 조합만 사용하세요");
            id_clean=false; 
            return; 
        }
        if(id == ''){
            alert('아이디를 입력해주세요.')
            id_clean=false;
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
                    id_clean=false;
                    $('#user_id').val('').focus();
                    return;
                }
                else{
                    $('#idbutton').attr("disabled", true);
                    alert("사용가능한 아이디입니다!");
                    id_clean=true;
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
        var email = $('#user_email').val()
        if(email == ''){
            alert('이메일을 입력해주세요.');
            email_clean=false;
            return;
        }
        if(email_regExp.test(email) == false){
            alert('이메일 형식을 맞춰주세요.');
            email_clean=false;
            return;
        }
        $.ajax({
            url:'emailvalid/',
            type:'get',
            dataType:'json',
            headers: {'X-CSRFToken': csrftoken},
            data:{email:email},
            success:function(){
                alert("인증번호가 전송되었습니다.");
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
                    {alert("인증에 성공하였습니다.");
                    email_clean=true;}}
                else {alert("인증번호가 일치하지 않습니다");
                    email_clean=false;}
                
            },
            error : function(xhr, error){
                alert("인증번호 전송을 실패했습니다.");
                console.error("error : " + error);
            }
        })
    })
})

var send = document.getElementById("send");
send.addEventListener("click", function () {
    var user_sex = document.getElementById("user_sex");
    var user_name = document.getElementById("user_name");
    var user_birth;
    var birth_yy =document.getElementById("birthyy");
    var birth_mm =document.getElementById("birthmm");
    var birth_dd =document.getElementById("birthdd");
    user_birth=birth_yy+'-'+birth_mm+'-'+birth_dd;
    if(user_sex!=null){sex_clean=true;};
    if(user_birth!=null){birth_clean=true;};
    if(user_name!=null){name_clean=true;};
    var form = document.getElementById("form");
    if (id_clean==true&pw_clean==true&email_clean==true&sex_clean==true&birth_clean==true&name_clean==true){
        form.action = '';
        form.method = "POST";
        form.submit();}
    else{alert("유효하지 않은 정보가 존재합니다.")}
    
})