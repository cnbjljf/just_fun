// JavaScript Document


    //自执行函数，用于移动用户注册协议的面板，还有点小bug。
    $(function(){
//        页面加载完成之后自动执行
        $('#title').mouseover(function() {
            $(this).css('cursor','move');
        }).mousedown(function(e){
            console.log($(this).offset());
            var _event = e || window.event;
//            原始鼠标的位置
            var ord_x = _event.clientX;
            var ord_y = _event.clientY;

            var parent_left = $(this).parent().offset().left;
            var parent_top = $(this).parent().offset().top;

            $(this).bind('mousemove',function(e){
//                现在鼠标移动位置
                var _new_event = e ||window.event;
                var new_x = _new_event.clientX;
                var new_y = _new_event.clientY;

                var x = parent_left + (new_x - ord_x);
                var y = parent_top + (new_y - ord_y);
//                var x = new_x
//                var y = new_y

                $(this).parent().css('left',x+'px');
                $(this).parent().css('top',y+'px');
            }
            )
        }).mouseup(function(){
            $(this).unbind('mousemove');
        });
    });


    var InterValObj; //timer变量，控制时间
    var count = 60; //间隔函数，1秒执行
    var curCount;//当前剩余秒数
    var codeLength = 6;//验证码长度

    //这个方法：判断用户输入是什么类型的，是邮箱注册还是手机注册，然后通过ajax和后台交互，发送验证码
    function sendMessage() {
        curCount = count;
        var phone = $.trim($('#phoneNo').val());//手机号码
        var CertType = "00";
        console.log(isMail(phone),isMoblie(phone));
        //flaghere 是标志位，匹配到了哪个就把flaghere设置为1，表示匹配到了，itype就等于这个匹配项
        if(isMoblie(phone)){
            var Itype='phone';
            register_type = 'phone';
            flaghere=1
        }else if(isMail(phone)){
            var Itype='email';
            register_type = 'phone';
            flaghere=1
        }else{
            flaghere=0
        }
        if(flaghere==1){
             //设置button效果，开始计时
            $("#btnSendCode").removeAttr("onclick");
            $("#btnSendCode").text(curCount + "s");
            InterValObj = window.setInterval(SetRemainTime, 1000); //启动计时器，1秒执行一次
            //向后台发送处理数据
            $.ajax({
                type: "GET", //用GET方式传输
                dataType: "json", //数据格式:JSON
                url: '/generateRegistPhoneRandCode', //目标地址
                data : {
                    type : Itype,
                    phoneNo : phone,
                },
                success : function(data) {
                    if(data.message == '该手机号码/邮箱地址已经被注册'){
                        window.clearInterval(InterValObj);
                        $("#btnSendCode").text("获取验证码");
                        $("#btnSendCode").attr("onclick","return sendMessage();");//启用按钮
                    }
                    alert(data.message);
                },
                error : function() {
                    alert('验证码发送失败，请重新发送');
                    return false;
                }
            });
        }else{
            alert("无效的手机号码、或者邮箱地址不符合常规格式")
        }
    }

    //timer处理函数，
    function SetRemainTime() {
        if (curCount == 0) {
            window.clearInterval(InterValObj);//停止计时器
            $("#btnSendCode").attr("onclick","return sendMessage();");//当倒计时为0的时候，启用按钮
            $("#btnSendCode").text("重获验证码");
        }
        else {
            //自减一，然后显示在发送验证码的方框内
            curCount--;
            $("#btnSendCode").text(curCount + "s");
        }
    }
    // check password
    var passwordIs = true;
    //keyup的方法是说每按下一个按键，都会去调用keyup后面的方法
    $('#Password').keyup(function(a) {
        var psw = $.trim($("#Password").val());
        //判断密码是否为中文
        if(!isChn(psw)){
            $(".pwd .pwd_grade").html(
            '<i class="i-warning"></i>密码不能包含中文').show();
            return;
        }
        var b = $(".pwd .pwd_grade");
        var thelev = checkPwd();
        //匹配checkPwd返回的的值
        switch (thelev) {
        case 1:
            passwordIs = true;
            b.html('安全程度：<i class="em em-thin"></i>');
            //b.html("安全程度:<strong class='pwdstron'></strong>")
            break;
        case 2:
            passwordIs = true;
            b.html('安全程度：<i class="em em-normal"></i>');
            //            b.html("安全程度:<strong class='pwdstron'></strong>")
            break;
        case 3:
            passwordIs = true;
            b.html('安全程度：<i class="em em-strong"></i>');
            //            b.html("安全程度:<strong class='pwdstron'></strong>")
            break;
        default:
            passwordIs = false;
            b.html('<i class="i-warning"></i>密码长度不能小于8位')
        }
    });

    //利用三目运算对密码强度做判断
    function checkPwd() {
        var a = $("#Password").val();
        return a.length >= 8 ? /[a-zA-Z]+/.test(a) && /\W+/.test(a) ? 3
                : /[a-zA-Z]+/.test(a) || /\W+/.test(a) ? 2 : 1 : 0
    }
    // verify password
    $("#VerifyPassword").blur(
            function() {
                var a = $(this).val();
                if ($.trim(a) == '') {
                    $(".pwd2 .pwd_grade").show().html(
                            '<i class="i-warning"></i>密码不能为空');
                    passwordIs = true;
                    return false;
                }
                if (a.length >= 8 && a == $("#Password").val()) {
                    passwordIs = true;
                    $(".pwd2 .pwd_grade").show().html(
                            '<i class="i-correct"></i>');
                } else if (!(a == $("#Password").val())) {
                    passwordIs = false;
                    $(".pwd2 .pwd_grade").show().html(
                            '<i class="i-warning"></i>两次密码输入不一致');
                }

                //$(".pwd2 .pwd_grade").show().html(a.length >= 8 && a == $("#Password").val() ? '<i class="i-correct"></i>': '<i class="i-warning"></i>两次密码输入不一致');
            });

    function checkData() {
        var registPassword = $("#Password").val();
        var phoneNo = $("#phoneNo").val();
        var registVerifyPassword = $("#VerifyPassword").val();
        var phoneRandCode = $("input[name=phoneRandCode]").val();
        if(isMoblie(phoneNo)){
            var register_type='phone'
        }else  if(isMail(phoneNo)){
            var register_type='email'
        }else{
            alert("无效的手机号码或者电子邮箱！！");
            return false;
        }
        //判断验证码为空
        if ($.trim(phoneRandCode) == '') {
            $("#code-span").show();
            alert("验证码不能为空");
            $("#phoneRandCode").focus();
            return false;
        } else {
            $("#code-span").hide();
        }
        //判断密码是否为空
        if ($.trim(registPassword) == '') {
            var b = $(".pwd .pwd_grade").html(
                    '<i class="i-warning"></i>密码不能为空').show();
            $("input[name=registPassword]").focus();
            return false;
        }
        //indexof等于python 的find，如果搜索出来的空格数大于等于0，那么就抛错
        if ($.trim(registPassword).indexOf(" ") >= 0) {
            console.debug($.trim(registPassword).indexOf(" "));
            var b = $(".pwd .pwd_grade").html(
                    '<i class="i-warning"></i>包含空格')
            $("input[name=registPassword]").focus();
            return false;
        }

        if (!(isChn(registPassword))) {
            var b = $(".pwd .pwd_grade").html(
                    '<i class="i-warning"></i>密码不能为中文')
            $("input[name=registPassword]").focus();
            return false;
        }

        //通过length方法来判断长度的
        if (registPassword.length < 8) {
            $(".pwd2 .pwd_grade").show().html(
                    '<i class="i-warning"></i>密码长度不能小于8位');
            $("input[name=registPassword]").focus();
            return false;
        }

        //对第二次输入的密码进行判断是否为空
        if ($.trim(registVerifyPassword) == '') {
            $(".pwd2 .pwd_grade").show().html(
                    '<i class="i-warning"></i>密码不能为空');
            $("input[name=registVerifyPassword]").focus();
            return false;
        }

        //对第二次输入的密码进行判断
        if (!(isChn(registVerifyPassword))) {
            $(".pwd .pwd_grade").html(
                    '<i class="i-warning"></i>密码不能为中文')
            $("input[name=registVerifyPassword]").focus();
            return false;
        }

        if (!(registPassword == registVerifyPassword)) {
            $(".pwd2 .pwd_grade").show().html(
                    '<i class="i-warning"></i>两次密码输入不一致');
            $("input[name=registVerifyPassword]").focus();
            return false;
        }

        //获取第一个check-box的值，如果没有选中，那么就提示要求选中
        if ($(".readme-checkbox").get(0).checked == false) {
            $("#readme-span").show();
            $("#readme_error_icon").show();
            $("span[name=readme_error]").text('请接受协议条款');
            $("input[id=readme]").focus();
            return false;
        } else {
            $("#readme-span").hide();
        }
        return true;
    }

    function protocolReg(){
        if ($(".readme-checkbox").get(0).checked == false) {
            $("[name='readme']").attr("checked",'true');//全选
        }
        document.getElementById('light').style.display='none';
        document.getElementById('fade').style.display='none';
    }

    //验证是否为邮箱
    function  isMail(tel){
        var regmail = /^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/g;
        if(!regmail.test(tel)){
            return false;
        }else{
            return true;
        }
    }





    //验证手机号码是否正确
    function isMoblie(tel) {
        //把正则表达式赋值给一个变量
        var reg = /^1((3[0-9])||(5[0-9])||(8[0-9])||(4[0-9])||(7[0-9]))\d{8}$/g;
        //用手机号码进行匹配
        if (!reg.test(tel)) {
            return false;
        } else {
            return true;
        }
    }
    //重置按钮调用这个方法
    function clearData() {
        //把所有的数据进行清空
        $("input[name=registName]").val('');
        $("input[name=registPassword]").val('');
        $("input[name=registVerifyPassword]").val('');
        $("#phoneRandCode").val('');
        $("#phoneNo").val('');
    }

    // 检查是否为中文
    function isChn(str) {
        var reg = /^.*[\u4e00-\u9fa5]+.*$/;
        if(reg.test(str)){
            return false;
        }else{
            return true;
        }
    }

//提交数据的先这么写，我也不知道对不对，等学完django后再做提交
$(function() {
        $("#sendRegister").click(function(){
            if(checkData()){
                //serialize方法能够序列化表单值，创建 URL 编码文本字符串
                $.post("/regist",$("form").serialize(),function(data){
                    if(data.status == 1){
                        alert("注册成功，跳转登录页面");
                        window.location = "/login";
                    }else{
                        alert(data.message);
                    }
                },"json");
            }
        });
    });
	
	
