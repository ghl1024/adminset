
from django.shortcuts import render, HttpResponse
from monitor.api import GetSysData
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from cmdb.models import Host
from lib.common import get_dir
import time
TIME_SECTOR = (
    86400*7,
    86400*14,
    86400*30,
    86400*60,
)


@login_required()
@permission_verify()
def index(request):
    return render(request, "monitor/manage.html", locals())


@login_required()
@permission_verify()
def drop_sys_info():
    """
    :drop sys_info db
    """
    db = GetSysData.connect_db()
    db.drop_database(get_dir("mongodb_collection"))
    return HttpResponse("ok")


@login_required()
@permission_verify()
def del_monitor_data(request, timing):
    timing = int(timing)
    if timing == 4:
        db = GetSysData.connect_db()
        db.drop_database("sys_info")
    else:
        host_list = Host.objects.all()
        client = GetSysData.connect_db()
        db = client.sys_info
        for host in host_list:
            try:
                collection = db[host]
            except:
                continue
            now_time = int(time.time())
            del_time = now_time-TIME_SECTOR[int(timing)]
            collection.delete_many({'timestamp': {'$lte': del_time}})
    return HttpResponse("ok")
