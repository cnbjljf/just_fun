from django.shortcuts import render
from housework import models

# Create your views here.

def login(request):
    return render(request,'login.html')

def index(request):
    return  render(request,'index.html')

def test(request):
    if request.method=='POST':
        print(request.POST)
        print('create data ok')
    return render(request,'test.html')

def hw(request):
    return render(request,'house_work.html')



def resource_manage(request):
    if request.method == 'POST':
        print(request.POST)
        hostname=request.POST['hostname']
        hostip = request.POST['hostip']
        hoststatus = request.POST['status']
        hostport = request.POST['hostport']
        action=request.POST['action']
        if action=='提交':
             # 先判断是否存在这条记录，如果存在那么久更新操作，不存在就创建
             if models.HostInfo.objects.filter(hostip=hostip):
                 models.HostInfo.objects.filter(hostip=hostip).update(hostname=hostname,hostip=hostip,port=hostport,status=hoststatus)
             else:
                 models.HostInfo.objects.create(hostname=hostname,hostip=hostip,port=hostport,status=hoststatus)
        elif action=='删除':
            models.HostInfo.objects.filter(hostip=hostip).delete()
        print('x'*10)
    host_info = models.HostInfo.objects.all()
    return render(request,'resource_manager.html',{'host_info':host_info})

def register(request):
    return render(request,'zhuche.html')