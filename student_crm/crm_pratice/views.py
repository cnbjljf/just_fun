from django.shortcuts import render
from crm_pratice import models
from django.http import HttpResponse
from django.core.paginator import  Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponseRedirect
from crm_pratice import forms
from django.core.urlresolvers import  resolve

# Create your views here.

# 定义一个字典，用来匹配要做什么样的操作。
action_list ={'Save':'save_data',
            'Del':'del_data',
            "Add_Record":"add_data"}


err_code = {
    401 : u'Error Data,Please try it again!!您输入的信息有误，请确认输入完整后再保存',
}
user_group={
    'common':['ljf'],
    'admin':['admin']
}


# 这个字典是用来处理权限的，new 为url包含的字段，GET为请求方式,第三列列表为URL附带的参数，第四列是要对哪些用户判断
permission_dic = {
    'use_add_record':['new','GET',[],user_group['common']],
}

def judge_permission(*args,**kwargs):
    '''
    该方法是用来进行权限判断的
    :param args:
    :param kwargs:
    :return:
    '''
    request = args[0]
    url_resolve_obj = resolve(request.path_info)
    current_url_name = url_resolve_obj.url_name
    print('url name now',current_url_name)
    matched_flag = False
    match_perm_key = None

    if current_url_name is not None:
        for perm_key in permission_dic:
            perm_val = permission_dic[perm_key]
            if len(perm_key) == 3:
                url_name,requst_method,requst_args = perm_val
                print(url_name,current_url_name)
                if url_name ==current_url_name:
                    if request.method == requst_method:
                        if not requst_args:
                            matched_flag == True
                            match_perm_key = perm_key
                            break
                        else:
                            for request_arg in requst_args:
                                request_method_func = getattr(request,requst_method)

                                if request_method_func.get(request_arg) is not None:
                                    matched_flag = True
                                else:
                                    matched_flag = False
                                    print("request arg [%s] not matched" % request_arg)
                                    break
                            if matched_flag == True:
                                match_perm_key = perm_key
                                print("--passed permission check--")
                                break
                    else:
                        return True

                    if matched_flag == True:
                        perm_str = 'crm.%s' %(match_perm_key)
                        if request.user.has_perm(perm_str):
                            print("\033[42;1m--------passed permission check----\033[0m")
                            return True
                        else:
                            print("\033[41;1m ----- no permission ----\033[0m")
                            print(request.user.perm_str)
                            return False
                    else:
                        print("\033[41;1m ----- no matched permission  ----\033[0m")


def check_permission(func):
    def wrapper(*args,**kwargs):
        if not judge_permission(*args,**kwargs):
            return render(args[0],'dashboard/403.html')
        return func(*args,**kwargs)
    return wrapper



def get_modes_func(request,func,fm_class,action,data_id):
    '''
    用来处理数据库信息的方法，增删改查等
    :param func:  modes里的方法名
    :param fm_class: 调用form 里面的哪个类
    :param action:  执行什么样的操作
    ;:param data_id: 获取哪个ID的数据
    :return:
     customer_obj = models.Customer.objects.get(id=customer_id)
     form = forms.CustomerModelForm(request.POST,instance=customer_obj)
    '''
    # func 是一个数据库的名字（modes里的方法名），
    if hasattr(models,func):
        func_obj = getattr(models,func)
    else:
        return False

    if hasattr(forms,fm_class):
        fm_class_obj = getattr(forms,fm_class)
    else:
        return False

    # 如果是查询所有的数据，那么走下面的代码
    if action == 'select_all_data':
        result = func_obj.objects.all()
        return result
    elif action == "fomr_get_all_data":
        fm_class_obj()
        return fm_class_obj()
    elif action == 'select_one_data':
        result =  func_obj.objects.get(id=data_id)
        form = fm_class_obj(instance=result)
        return form
    elif action == 'save_data':
        result_obj = func_obj.objects.get(id=data_id)
        fm = fm_class_obj(request.POST,instance=result_obj)
        fm.save()
        return True
    elif action == "del_data":
        #models.Customer.objects.filter(qq=request.POST.get('qq')).delete()
        func_obj.objects.filter(id=data_id).delete()
        print('Delete this Record ......')
        return True
    elif action == "add_data":
        fm_result = fm_class_obj(request.POST)
        if fm_result.is_valid():
            fm_result.save()
        return  True


def add_new_info(request,form_class,html_page,html_pass_info):
    '''
    这个方法主要用来处理新添记录的，
    :param request:
    :param form_class: 使用form里面的哪个类
    :param html_page:  返回的网页
    :param html_pass_info:  网页中jinja需要的数据
    :return:
    '''
    if hasattr(forms,form_class):
        form_func = getattr(forms,form_class)
    else:
        return False
    if request.method == 'POST':
        form = form_func(request.POST)
        if form.is_valid():
            form.save()
            base_url = '/'.join(request.path.split("/")[:-2])
            print('base_url',base_url)
            # redirect to uplevel page!!
            return HttpResponseRedirect(base_url)
        else:
            # 401 means POST data is not complete
            return HttpResponse(err_code.get(401))
    form = form_func()
    return render(request,html_page,{html_pass_info:form})



def paging(request,models_func):
    '''
    此方法用来处理分页的
    :param models_func : models里面的方法，也就是库名
    :return:内容
    '''
    if hasattr(models,models_func):
        func = getattr(models,models_func)
        ct_list = func.objects.all()
    else:
        return False
    # show 2 contacts per page
    paginator = Paginator(ct_list,10)
    page = request.GET.get('page')
    try:
        customer_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        customer_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range(e.g 9999),deliver last page of result
        customer_list = paginator.page(paginator.num_pages)
    return customer_list


def acc_login(request):
    '''
    这个方法用来处理 登陆请求的
    :param request:
    :return:
    '''
    if request.method == 'POST':
        print(request.POST)
        authcode = request.POST.get('authcode')
        user = authenticate(username=request.POST.get('loginname'),
                                   password=request.POST.get('nloginpwd'))
        if authcode.lower() == 'k9ra':
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/crm')
            # else:
            #     render(request,'stu_info/login1.html')

    return render(request,'dashboard/login1.html')


def acc_logout(requstion):
    '''
    这个方法用来处理退出登陆请求
    :param requstion:
    :return:
    '''
    logout(requstion)
    return HttpResponseRedirect('/crm')


@login_required()
def dashboard(request):
    return  render(request,'dashboard/index.html')

#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# 以下几个负责处理客户信息管理的
@login_required()
def detail_per_customer(request,customer_id):
    # 从数据库里面获取该客户ID的值
    print('---->',customer_id)
    '''
     ----------> Dropping this code of reason is too long and duplicated code
    # customer_obj = models.Customer.objects.get(id=customer_id)
    # if request.method == 'POST':
    #     print(request.POST)
    #     # Save is means update this record!
    #     if request.POST.get('action') == 'Save':
    #         form = forms.CustomerModelForm(request.POST,instance=customer_obj)
    #         form.save()
    #         return   HttpResponseRedirect('/crm/customer')
    #     elif request.POST.get('action') == 'Del':
    #         models.Customer.objects.filter(qq=request.POST.get('qq')).delete()
    #         return   HttpResponseRedirect('/crm/customer')
    #     elif request.POST.get('action') == 'Add_Record':
    #         form=forms.CustomerModelForm(request.POST)
    #         form.save()
    # else:
    #     form = forms.CustomerModelForm(instance=customer_obj)
    '''

    # 获取所有的数据
    form = get_modes_func(request,func='Customer',fm_class='CustomerModelForm',action='select_one_data',data_id=customer_id)
    if request.method == 'POST':
            #通过字典去匹配要执行的动作。
            print('-------->',request.POST,'11111111',request.POST.get('action'))
            form = get_modes_func(request,func='Customer',fm_class='CustomerModelForm',
                                  action=action_list.get(request.POST.get('action')),
                                  data_id=customer_id)
            if form:return HttpResponseRedirect('/crm/customer')
            else:return render(request,u'操作失败，请重新尝试一次')

    return render(request,'dashboard/customer_detail.html',{'customer_form':form})


#@check_permission(judge_permission)
@login_required()
def add_new_customer(request):
    '''
    z这个方法用来处理新添客户信息的
    if request.method == 'POST':
            form = forms.CustomerModelForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/crm/customer')
            else:
                return HttpResponse(err_code.get(401))

    form = forms.CustomerModelForm()
    return   render(request,'dashboard/customer_detail.html',{'customer_form':form})
    '''
    return add_new_info(request,form_class='CustomerModelForm',
                 html_page='dashboard/customer_detail.html',
                 html_pass_info='customer_form')


@login_required()
def customer(request):
    customer_list = paging(request,'Customer')
    return render(request,'dashboard/customer.html',{'customer_list':customer_list})

#  ======================================== 华丽分割线 ===================================
# 以下几个处理班级列表信息的
@login_required()
def classes(request):
    class_list = paging(request,'ClassList')
    return render(request,'dashboard/classes.html',{'class_list':class_list})

@login_required()
def detail_per_class(request,class_id):
    # class_obj = models.ClassList.objects.get(id=class_id)
    if request.method == "POST":
        print(request.POST)
        get_modes_func(request,func='ClassList',fm_class='ClassModelForm',
                       action=action_list.get(request.POST.get('action')),
                       data_id=class_id)
        return HttpResponseRedirect('/crm/classes')
    # form = forms.ClassModelForm(instance=class_obj)
    form = get_modes_func(request,func='ClassList',fm_class='ClassModelForm',
                          action='select_one_data',data_id=class_id)
    return render(request,'dashboard/class_detail.html',{'class_info':form})

@login_required()
def add_new_class(request):
    '''
    这个是用来处理添加新的班级列表的内容，
    # if request.method == 'POST':
    #     print(request.POST)
    #     form = forms.ClassModelForm(request.POST)
    #     if form.is_valid:
    #         form.save()
    #     else:
    #         return HttpResponse(err_code.get(401))
    # form = forms.ClassModelForm()
    # return render(request,'dashboard/class_detail.html',{'class_info':form})
    '''
    return add_new_info(request,form_class='ClassModelForm',
                 html_page='dashboard/class_detail.html',
                 html_pass_info='class_info')


# ======================华丽分割线-============================
# 以下方法是处理 用户，讲师信息的
@login_required()
def teacher(request):
    form = get_modes_func(request,func='UserProfile',fm_class='UserProfileModelForm',
                       action='select_all_data',
                       data_id=None)
    return render(request,'dashboard/teachers.html',{'user_list': form})

def add_new_teacher(request):
    return add_new_info(request,form_class='UserProfileModelForm',
                        html_page="dashboard/teachers_detail.html",
                        html_pass_info='user_list'
                        )
@login_required()
def detail_per_teacher(request,class_id):
    # class_obj = models.ClassList.objects.get(id=class_id)
    if request.method == "POST":
        print(request.POST)
        get_modes_func(request,func='UserProfile',fm_class='UserProfileModelForm',
                       action=action_list.get(request.POST.get('action')),
                       data_id=class_id)
        return HttpResponseRedirect('/crm/teachers')
    # form = forms.ClassModelForm(instance=class_obj)
    form = get_modes_func(request,func='UserProfile',fm_class='UserProfileModelForm',
                          action='select_one_data',data_id=class_id)
    return render(request,'dashboard/teachers_detail.html',{'user_list':form})

# ======================华丽分割线-============================
# 以下方法是处理 学生成绩的信息的
@login_required()
def stu_grade(request):
    form = get_modes_func(request,func='StudyRecord',fm_class='StudyRecordModelForm',
                          action='select_all_data',
                          data_id=None)
    return render(request,'dashboard/stu_grade.html',{'stu_grade':form})

@login_required()
def add_new_StuRec(request):
    print('xx'*100)
    return add_new_info(request,form_class='StudyRecordModelForm',
                        html_page="dashboard/stu_grade_detail.html",
                        html_pass_info='stu_grade',
                        )

@login_required()
def detail_per_StuRec(request,student_id):
    print('xx'*100)
    # class_obj = models.ClassList.objects.get(id=class_id)
    if request.method == "POST":
        print(request.POST)
        get_modes_func(request,func='StudyRecord',fm_class='StudyRecordModelForm',
                       action=action_list.get(request.POST.get('action')),
                       data_id=student_id)
        return HttpResponseRedirect('/crm/stu_grade')
    form = get_modes_func(request,func='StudyRecord',fm_class='StudyRecordModelForm',
                          action='select_one_data',data_id=student_id)
    return render(request,'dashboard/stu_grade_detail.html',{'stu_grade':form})