// JavaScript Document
(function($){
			
			$(function(){
				if(""){
	 				//$('.sign_box').slideDown(300).delay(3000).fadeOut(1000);
                    alert('aaa')
				}
				// > 代表着item下面的所有input标签
				$(".item > input").focusin(function(){
					$(this).parent().addClass("item-focus");
					$(".item").removeClass("item-error");
					$(".msg-warn").show();
					$(".msg-error").hide();
				});

				$(".item > input").blur(function(){
					$(this).parent().removeClass("item-focus");
				});
                //当键盘回车时（case==13），那么就让提交按钮提交
				$(".item > input").keydown(function(event){
					switch(event.keyCode) {
						case 13:
							$("#btnSubmit").click();
							break;
				 	 }
				});
				var flag = true;
				$("#formlogin").submit(function(){
					flag = true;
					var loginname=$("#loginname").val();
					var nloginpwd=$("#nloginpwd").val();
					var authcode=$("#authcode").val();
					if($.trim(loginname)==''){
						$("input[name=loginname]").parent().removeClass("item-focus");
						$("input[name=loginname]").parent().addClass("item-error");
                        //hide方法就是把被选元素是显示的就给隐藏
                        $(".msg-warn").hide();
                        //show方法就是把被选元素是隐藏的就给显示
                        $(".msg-error").show();
						$(".msg-error > span").text("账号名不能为空");
						flag = false;
					}else if($.trim(nloginpwd)==''){
						$("input[name=nloginpwd]").parent().removeClass("item-focus");
						$("input[name=nloginpwd]").parent().addClass("item-error");
						$(".msg-warn").hide();
						$(".msg-error").show();
						$(".msg-error > span").text("密码不能为空");
						flag = false;
					}else if($.trim(authcode)==''){
						$("input[name=authcode]").parent().removeClass("item-focus");
						$("input[name=authcode]").parent().addClass("item-error");
						$(".msg-warn").hide();
						$(".msg-error").show();
						$(".msg-error > span").text("验证码不能为空");
						flag = false;
					}
					return flag;
				});
				
				
				$("#btnSubmit").click(function(){
					$("#formlogin").submit();
					if(flag){
						var account = $("#loginname").val();
						var password = $("#nloginpwd").val();
						var authcode = $("#authcode").val();
						$.ajax({
							url : '/login',
							type : 'post',
							data : {
								account : account,
								password : password,
								authcode : authcode
							},
							dataType : 'json',
							success : function(data) {
								var message = decodeURI(data.message);
								if (message && message != "null"){
									$(".msg-warn").hide();
									$(".msg-error").show();
									$(".msg-error > span").text(message);
									flag = false;
                                     //设定属性，打上时间戳
									$("#FC_Verification1").attr("src",'/captcha?' + (+ new Date()));
								}
								else
									window.location.href = '/home';
							},
							error : function() {
                                $('.msg-error').hide();
                                $('.msg-error').show();
                                $(".msg-error > span").text("用户名或密码或验证码错误！");
                                //设定属性，打上时间戳
								$("#FC_Verification1").attr("src",'/captcha?' + (+ new Date()));
							}
						});
					}
				});
				
			});
		})(jQuery);