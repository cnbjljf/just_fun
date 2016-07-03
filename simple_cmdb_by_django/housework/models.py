from django.db import models


# Create your models here.

# 创建主机表
class HostInfo( models.Model ):
    hostname = models.CharField( max_length=108 )
    hostip = models.GenericIPAddressField(max_length=100)
    port = models.IntegerField()
    status = models.CharField( max_length=64 )
