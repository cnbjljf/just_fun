/**
 * Created by ljf on 2016/4/29 0029.
 */

    function become_active(ele){
        $(ele).addClass('active').
        $(ele).siblings().removeClass('active')
        alert(ele)
}

//    这个函数是用来启动编辑作用的函数
    function edit(id) {
//        首先把修改框的隐藏样式给去除
        $('#submit_form').removeClass('hide');
//        以下三行是把现有的内容提出来，等会放到修改框里面去，
        var cur_port = $(id).parent().siblings().children('.port').text();
        var cur_hostname = $(id).parent().siblings().children('.hostname').text();
        var cur_status = $(id).parent().siblings().children('.status').text();

//        下面几步都是通过替换的方式，把当前要编辑的一行信息替换到编辑框里面去
        $('#in_hostname').replaceWith('<input  id="in_hostname" type="text" value='+cur_hostname +'>');
        $('#in_port').replaceWith('<input  id="in_port" type="text" value='+cur_port +'>');
        $('#in_status').children('option').each(function(index,element){
//            下面执行一个判断语句，判断当前服务器状态等于下拉列表中的哪个，如果匹配上了，那么就把下拉列表里面的匹配到\
//            状态添加上selected=selected参数
           if (cur_status == $(element).val() ){
               $(element).replaceWith("<option selected='selected'>"+cur_status+"</option>")
           }});
//        标记位，标志着用户是对哪个内容做更改
        $(id).attr('id','on_modify');
    }

//    这个函数是用来更改input type=check 的checked值，选中了就是true
    function choose_it(id) {
        if (!$(id).attr('checked')) {
            $(id).attr('checked', true)
        }else{
             $(id).attr('checked', false)
        }
    }

//    这个方法用来判断用户有没有勾选 复选框
    function check_gou(){
        i=0
        $('input[type="checkbox"]').each(function(index,element){
            if($(element).attr('checked')=='checked'){
//                勾选了就加1
                i+=1
            }
        });
        if (i != 0) {
            return true
        } else {
            alert("您没有勾选任何列表，请先勾选列表！")
            return false
        }

    }
//    这个函数在批量编辑的时候使用
    function mul_edit() {
        if(check_gou()){
        $('input[type="checkbox"]').each(function(index,element) {
            if ($(element).attr('checked') == 'checked') {
                var cur_port = $(element).parent().siblings().children('.port').text();
                var cur_hostname = $(element).parent().siblings().children('.hostname').text();
                var cur_status = $(element).parent().siblings().children('.status').text();
                //        下面几步都是通过替换的方式，把当前要编辑的一行信息替换到编辑框里面去

                $(element).parent().siblings().children('.hostname').replaceWith('<input class="hostname"  type="text" value=' + cur_hostname + '>');
                $(element).parent().siblings().children('.port').replaceWith('<input class="port"  type="text" value=' + cur_port + '>');
                $(element).parent().siblings().children('.status').replaceWith('<input  class="status" type="text" placeholder="下线/上线/维护" value=' + cur_status + '>');
            }
            $('#save_edit').removeClass('hide');
            $('#cancel_edit').removeClass('hide')
        })
        };
    }

//    这个方法用来保存批量编辑的
    function mul_edit_save() {
        $('input[type="checkbox"]').each(function(index,element){

            if($(element).prop('checked')){
                var cur_port = Number($(element).parent().siblings().children('.port').val().trim());
                var cur_hostname = $(element).parent().siblings().children('.hostname').val().trim();
                var cur_status = $(element).parent().siblings().children('.status').val().trim();
                var port_match = /^\d+$/
                var hostname_match = /^\w+\-\w+\-[\d+|\w+|\w+\d+|\d+\w]+\-[\w+\d|\d+\w]+$/
                console.log("hostname match",hostname_match.test(cur_hostname))
                if(!port_match.test(cur_port) ){
                    alert("你输入的端口不对！应该输入数字")
                    return false
                }
                if(!hostname_match.test(cur_hostname)){
                    alert("你输入的主机名不符合公司规范，请更正！")
                    return false
                }
                if(cur_hostname && cur_port && cur_status){
                    $(element).parent().siblings().children('.hostname').replaceWith('<div class="hostname">'+cur_hostname +'<div>');
                    $(element).parent().siblings().children('.port').replaceWith('<div class="port">'+cur_port +'<div>');
                    $(element).parent().siblings().children('.status').replaceWith('<div class="status">'+cur_status +'<div>');
                    $(element).prop('checked', false);
                    flaga=0;
                }else{
                    alert('请输入内容,框内不能有空');
                    flaga=1;
                    return false
                }
//                if(cur_hostname && cur_port && cur_status){
//        //        下面几步都是通过替换的方式，把当前要编辑的一行信息替换到编辑框里面去

//    //                $('#save_edit').addClass('hide');
//    //                $('#cancel_edit').addClass('hide')
//                }else{
//                    alert('请输入内容,框内不能有空');
//                    return false
//                }
            };
        });
        if(flaga!=1){
            $('#save_edit').addClass('hide');
            $('#cancel_edit').addClass('hide')

        }else{
            $('#save_edit').removeClass('hide');
            $('#cancel_edit').removeClass('hide')
        }

    }

    function mul_edit_cancel() {
        $('input[type="checkbox"]').each(function(index,element){
            if($(element).attr('checked')=='checked'){
    //        下面几步都是通过替换的方式，把当前要编辑的一行信息替换到编辑框里面去
            var cur_port = $(element).parent().siblings().children('.port').val();
            var cur_hostname = $(element).parent().siblings().children('.hostname').val();
            var cur_status = $(element).parent().siblings().children('.status').val();

            $(element).parent().siblings().children('.hostname').replaceWith('<div class="hostname" >'+cur_hostname +'</div>');
            $(element).parent().siblings().children('.port').replaceWith('<div class="port">'+cur_port +'</div>');
            $(element).parent().siblings().children('.status').replaceWith('<div class="status">'+cur_status +'</div>');
            }});
        $('#save_edit').addClass('hide');
        $('#cancel_edit').addClass('hide')
    }



//    全部选中的方法
    function QuanXuan() {
//        alert('全部选中')
        $('input[type=checkbox]').prop('checked',true)
        $('input[type=checkbox]').attr('checked',true)
    }

//  全部不选中的方法
    function QuanBuXuan() {
//        alert('全部不选')
         $('input[type=checkbox]').prop('checked',false)
        $('input[type=checkbox]').attr('checked',false)
    }

//    全部反选的方法
    function FanXuan() {
//        alert('全部反选')
//        each表示遍历所有的值（each前面的内容就是需要遍历的值），each后面跟着的括号就是遍历一次需要执行什么操作
        $('input[type=checkbox]').each(function() {
            $(this).prop('checked', !$(this).attr('checked'))
            $(this).attr('checked', !$(this).attr('checked'))
        })}

//    在修改框内提交按钮时调用此方法，主要是对输入内容的判断，如果有内容就把表格里面替换成修改后的，没有输入内容题提示输入
    function checkCon() {
        var host_name = $('#in_hostname').val();
        var host_port = $('#in_port').val();
        var host_status = $('#in_status').val();
        if(host_name,host_port){
    //        下面的是遍历需要编辑的主机名，端口，状态信息等，通过switch来匹配后赋值
            $('#on_modify').parent().siblings().children('div').each(function(index,element){
               switch($(element).attr('class')){
                   case 'hostname':
                       $(element).text(host_name);
                       break;
                   case 'port':
                       $(element).text(host_port);
                       break;
                   case 'status':
                       $(element).text(host_status);
                       break;
               }
            });
    //        删除标记位
            $('#on_modify').removeAttr('id');
            $('#submit_form').addClass('hide');
        }else{
            alert('请输入内容');
            return false
        }
    }

//    取消编辑修改框
    function Cancle_sm() {
        $('#submit_form').addClass('hide');
    }

//  增加表格
    function Add_frame(){
//        自定义一个数组
        var shuzu=[0]
//        遍历td下的input标签，主要把value值给提取出来
        $('td input').each(function(index,element){
            shuzu.push($(element).val())
        })
//        找出数组里面最大的值，为添加下面的html代码中赋值input的id和value值
        var maxzhi = Math.max.apply(null,shuzu)
        var use_value = Number(maxzhi)+1
//        在表单里的最后一个子元素里面插入html代码
        $('form table').children().last().after('<tr>\
        <td><input id="no'+use_value +'" type="checkbox" onclick="choose_it(this)" value='+use_value+'></td>\
        <td><div class="hostname"></div></td>\
        <td><div class="port"></div></td>\
        <td><div class="status"></div></td>\
        <td><div onclick="edit(this)">编辑</div></td>\
    </tr>')
    }

//    删除所选中的内容
    function Del_frame() {
        $('input[type=checkbox]').each(function(index,element) {
//            如果判断出这个input checked值为checked，表示已经选中了这个框，那么就执行下面的删除动作
            if( $(element).attr('checked')=='checked'){
//                提出选中框的id值
                var del_id = $(element).attr('id')
//                alert(del_id)
//                开始删除
                $('#'+del_id).parent().parent().remove()
                $('#'+del_id).parent().siblings().remove()
                $('#'+del_id).parent().remove()
                $('#'+del_id).remove()
            }
        })
    }
    function Func(a) {
        $(a).next().removeClass('hide');
        $(a).parent().siblings().find('.body').addClass("hide")
    }
