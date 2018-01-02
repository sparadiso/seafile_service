# Copyright (c) 2012-2016 Seafile Ltd.
from django.db import models
from django.utils import timezone

class UserLoginLogManager(models.Manager):
    def create_login_log(self, username, login_ip):
        l = super(UserLoginLogManager, self).create(username=username,
                                                    login_ip=login_ip)
        l.save()
        return l
        
class UserLoginLog(models.Model):
    username = models.CharField(max_length=255, db_index=True)
    login_date = models.DateTimeField(default=timezone.now, db_index=True)
    login_ip = models.CharField(max_length=128)
    objects = UserLoginLogManager()

    class Meta:
        ordering = ['-login_date']
        
########## signal handler
from django.dispatch import receiver
from seahub.auth.signals import user_logged_in
from seahub.utils.ip import get_remote_ip

@receiver(user_logged_in)
def create_login_log(sender, request, user, **kwargs):
    username = user.username
    login_ip = get_remote_ip(request)
    UserLoginLog.objects.create_login_log(username, login_ip)
    
    
