from .models import OpsLog

def savelog(user,command,host,result,details):
    opslog = OpsLog()
    opslog.user = user
    opslog.cmd = command
    opslog.host = host
    opslog.result = result
    opslog.details = details
    opslog.save()