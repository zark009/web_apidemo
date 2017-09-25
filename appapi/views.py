from django.shortcuts import render
from appapi.models import *
from django import template
from appapi.utils import *
from django.core import serializers
from django.http import HttpResponse
from django.template.loader import render_to_string
import os
import time, datetime
import random
from apscheduler.schedulers.blocking import BlockingScheduler


def hello(request):
    return render(request, "index.html")


def show_api_list(request):
    api_list = Interface.objects.order_by("-create_time")
    app_list = App.objects.all()
    page_list = AppPage.objects.all()
    return render(request, "apilist.html", {"apis": api_list, "apps": app_list, "pages": page_list})


def show_api_user(request):
    api_list = Interface.objects.filter(app_id=1).order_by("-create_time")
    app_list = App.objects.all()
    page_list = AppPage.objects.all()
    return render(request, "apilist.html", {"apis": api_list, "apps": app_list, "pages": page_list})


def show_api_driver(request):
    api_list = Interface.objects.filter(app_id=2).order_by("-create_time")
    app_list = App.objects.all()
    page_list = AppPage.objects.all()
    return render(request, "apilist.html", {"apis": api_list, "apps": app_list, "pages": page_list})


def get_page_data(request, offset):
    appid = int(offset)
    page_list = AppPage.objects.filter(app_id=appid)
    data = serializers.serialize('json', page_list)
    return HttpResponse(data, content_type='application/json')


def get_app_data(request):
    app_list = App.objects.all()
    data = serializers.serialize('json', app_list)
    return HttpResponse(data, content_type='application/json')


def app_list(request):
    app_list = App.objects.all()
    return render(request, "applist.html", {"apps": app_list})


def page_list(request):
    page_list = AppPage.objects.all()
    app_list = App.objects.all()
    return render(request, "pagelist.html", {"pages": page_list, "apps": app_list})


def add_app(request):
    if request.method == 'POST':
        name = request.POST.get("appname")

        id = int(App.objects.latest('id').app_id)
        app = App(app_name=name, app_id=id + 1)
        app.save()
    app_list = App.objects.all()
    return render(request, "applist.html", {"apps": app_list})


def add_page(request):
    if request.method == 'POST':
        appid = request.POST.get("appid")
        pagename = request.POST.get("pagename")
        pageid = int(AppPage.objects.filter(app_id=appid).latest('page_id').page_id)
        app = AppPage(page_name=pagename, page_id=pageid + 1, app_id=appid)
        app.save()
    page_list = AppPage.objects.all()
    return render(request, "pagelist.html", {"pages": page_list})


def edit_page(request):
    if request.method == 'POST':
        name = request.POST.get("pagename")
        pageid = request.POST.get("pageid")
        uptime = datetime.datetime.now()
        page = AppPage.objects.filter(page_id=pageid).update(page_name=name, update_time=uptime)
    page_list = AppPage.objects.all()
    return render(request, "pagelist.html", {"pages": page_list})


def edit_app(request):
    if request.method == 'POST':
        name = request.POST.get("appname")
        appid = request.POST.get("appid")
        uptime = datetime.datetime.now()
        api = App.objects.filter(id=appid).update(app_name=name, update_time=uptime)
    app_list = App.objects.all()
    return render(request, "applist.html", {"apps": app_list})


def show_api_case(request):
    case_list = ApiCase.objects.order_by("-create_time")
    api_list = Interface.objects.all()

    return render(request, "apicase.html", {"apis": api_list, "cases": case_list})


def run_api(request):
    apiid = request.POST.get('id')
    api = Interface.objects.get(id=apiid)
    api_cases = ApiCase.objects.filter(api_id=apiid)
    app_ver = api.app.app_id
    url = api.url
    if app_ver == 1:
        zoken = user_token()
    else:
        zoken = car_token()
    api.elapsed_time = 0
    for api_case in api_cases:
        if api_case.header == '':
            headers = api_case.header
        else:
            headers = api_case.header
            headers = re_header(headers, zoken)
        if api_case.in_param == '':
            requests_data = api_case.in_param
        else:
            requests_data = eval(api_case.in_param)
        try:
            req = requests.post(url, data=json.dumps(requests_data), headers=headers)
            if req.status_code == 200 and re.search(api_case.expect, req.text):
                api_case.status = 1
                api_case.elapsed_time = float(req.elapsed.microseconds) / 1000
                api_case.result = req.text
                api_case.execute_time = datetime.datetime.now()

                api.elapsed_time += api_case.elapsed_time

                api.status = 1
            else:
                api_case.status = 0
                api_case.elapsed_time = float(req.elapsed.microseconds) / 1000
                api_case.result = req.text
                api_case.execute_time = datetime.datetime.now()

                api.elapsed_time += api_case.elapsed_time

                api.status = 0

        except Exception as e:
            api_case.status = 0
            api_case.result = e
            api_case.execute_time = datetime.datetime.now()
            api_case.save()
            api.status = 0
        else:
            api.execute_time = datetime.datetime.now()
            api_case.save()
            api.save()
            id = api.id
            status = api.status
            eltime = api.elapsed_time
            extime = api.execute_time
            extime = extime.strftime('%Y-%m-%d %H:%M:%S')

    return HttpResponse(json.dumps({
        "id": id,
        "status": status,
        "eltime": eltime,
        "extime": extime

    }, ensure_ascii=False))


def run_api_case(request):
    id = request.POST.get('id')
    api_case = ApiCase.objects.get(id=id)
    api = Interface.objects.get(id=api_case.api_id)
    app_ver = api.app.app_id
    url = api.url
    if app_ver == 1:
        zoken = user_token()
    else:
        zoken = car_token()

    if api_case.header == '':
        headers = api_case.header
    else:

        headers = api_case.header
        headers = re_header(headers, zoken)

    if api_case.in_param == '':
        requests_data = api_case.in_param
    else:
        requests_data = eval(api_case.in_param)
    try:
        req = requests.post(url, data=json.dumps(requests_data), headers=headers)

        if req.status_code == 200 and re.search(api_case.expect, req.text):
            api_case.status = 1
            api_case.elapsed_time = float(req.elapsed.microseconds) / 1000
            api_case.result = req.text
            api_case.execute_time = datetime.datetime.now()

        else:
            api_case.status = 0
            api_case.elapsed_time = float(req.elapsed.microseconds) / 1000
            api_case.result = req.text
            api_case.execute_time = datetime.datetime.now()


    except Exception as e:
        api_case.status = 0
        api_case.result = e
        api_case.execute_time = datetime.datetime.now()
        api_case.save()

    else:
        api_case.save()
        id = api_case.id
        apiname = api_case.api.name
        casename = api_case.name
        checkpoint = api_case.expect
        status = api_case.status
        eltime = api_case.elapsed_time
        extime = api_case.execute_time
        extime = extime.strftime('%Y-%m-%d %H:%M:%S')
        result = api_case.result

    return HttpResponse(json.dumps({
        "id": id,
        "apiname": apiname,
        "casename": casename,
        "checkpoint": checkpoint,
        "status": status,
        "eltime": eltime,
        "extime": extime,
        "result": result
    }, ensure_ascii=False))


def add_api_case(request):
    if request.method == 'POST':
        api_id = request.POST.get("id")
        name = request.POST.get("casename")
        inparam = request.POST.get("inparam")
        header = request.POST.get("header")
        expect = request.POST.get("expect")
        api = Interface.objects.get(id=api_id)
        counts = str(int(api.case_count) + 1)

        api_case = ApiCase(name=name, in_param=inparam, header=header, expect=expect, api_id=api_id, elapsed_time=0,
                           result='')

        api_case.save()

        api = Interface.objects.filter(id=api_id).update(case_count=counts)

    case_list = ApiCase.objects.order_by("-create_time")
    api_list = Interface.objects.all()
    return render(request, "apicase.html", {"cases": case_list, "apis": api_list})


def edit_api_case(request):
    if request.method == 'POST':
        caseid = request.POST.get("id")
        name = request.POST.get("casename")
        inparam = request.POST.get("inparam")
        header = request.POST.get("header")
        expect = request.POST.get("expect")
        uptime = datetime.datetime.now()
        apicase = ApiCase.objects.filter(id=caseid).update(name=name, in_param=inparam, header=header, expect=expect,
                                                           update_time=uptime)

    return HttpResponse(json.dumps({
        "id": id,
        "name": name,
        "inparam": inparam,
        "header": header,
        "expect": expect}, ensure_ascii=False))
    # return render(request, "apicase.html", {"cases": case_list, "apis": api_list})


# 修改接口信息

def edit_api(request):
    if request.method == 'POST':
        apiid = request.POST.get("id")
        name = request.POST.get("apiname")
        desc = request.POST.get("apidescribe")
        url = request.POST.get("apiurl")
        appid = request.POST.get("appid")
        pageid = request.POST.get("pageid")
        api = Interface.objects.filter(id=apiid).update(name=name, summary=desc, url=url, app_id=appid, page_id=pageid)
    return HttpResponse(json.dumps({
        "name": name,
        "url": url,
        "appid": appid,
        "pageid": pageid,
    }, ensure_ascii=False))


def add_api(request):
    if request.method == 'POST':
        name = request.POST.get("apiname")
        desc = request.POST.get("apidescribe")
        url = request.POST.get("apiurl")
        appid = request.POST.get("appid")
        pageid = request.POST.get("pageid")
        api = Interface(name=name, summary=desc, url=url, case_count=0, elapsed_time=0, app_id=appid, page_id=pageid)
        api.save()
    api_list = Interface.objects.order_by("-create_time")
    app_list = App.objects.all()
    page_list = AppPage.objects.all()
    return render(request, "apilist.html", {"apis": api_list, "apps": app_list, "pages": page_list})


def test_add(request):
    if request.method == 'POST':
        for key in request.POST:
            print(key)
            valuelist = request.POST.getlist(key)
            print(valuelist)
    a = "dasdasdasddsad"
    return HttpResponse(HttpResponse(json.dumps(a), content_type='application/json'))


def test(request):
    return render(request, "applist.html")


def task_list(request):
    task_list = TaskList.objects.order_by("-create_time")
    return render(request, "tasklist.html", {"tasks": task_list})


def add_task(request):
    if request.method == 'POST':
        name = request.POST.get("taskname")
        taskid = str(int(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))) + str(random.randint(0, 99))
        casecount = 0
        passcount = 0
        failcount = 0
        estime = 0
        task = TaskList(task_name=name, task_id=taskid, case_count=casecount, pass_count=passcount,
                        fail_count=failcount, elapsed_time=estime)
        task.save()
        task_list = TaskList.objects.order_by("-create_time")

    return render(request, "tasklist.html", {"tasks": task_list})


def run_task(request):
    taskid = request.POST.get('id')

    apis = Interface.objects.all()
    pcount = 0
    fcount = 0
    ccount = 0
    tasklist_elapsed_time = 0

    for api in apis:
        app_ver = api.app.app_id
        pageid = api.page.page_id

        url = api.url

        if app_ver == 1:
            zoken = user_token()
        else:
            zoken = car_token()
        api_cases = ApiCase.objects.filter(api_id=api.id)
        for api_case in api_cases:
            caseid = api_case.id
            ccount += 1
            if api_case.header == '':
                headers = api_case.header
            else:
                headers = api_case.header
                headers = re_header(headers, zoken)
            if api_case.in_param == '':
                requests_data = api_case.in_param
            else:
                requests_data = eval(api_case.in_param)
            try:
                req = requests.post(url, data=json.dumps(requests_data), headers=headers)
                if req.status_code == 200 and re.search(api_case.expect, req.text):
                    task_status = 1
                    task_in_param = api_case.in_param
                    task_expect = api_case.expect
                    task_header = api_case.header
                    task_elapsed_time = float(req.elapsed.microseconds) / 1000000
                    task_result = req.text
                    task_execute_time = datetime.datetime.now()
                    pcount += 1

                    tasklist_elapsed_time += task_elapsed_time
                    tasklist_elapsed_time = round(tasklist_elapsed_time, 2)

                else:
                    task_status = 0
                    task_elapsed_time = float(req.elapsed.microseconds) / 1000000
                    task_in_param = api_case.in_param
                    task_expect = api_case.expect
                    task_header = api_case.header
                    task_result = req.text
                    task_execute_time = datetime.datetime.now()
                    fcount += 1
                    tasklist_elapsed_time += task_elapsed_time
                    tasklist_elapsed_time = round(tasklist_elapsed_time, 2)


            except Exception as e:
                fcount += 1
                task_status = 0
                task_result = e
                task_in_param = api_case.in_param
                task_expect = api_case.expect
                task_header = api_case.header
                task_execute_time = datetime.datetime.now()
                tasklist_elapsed_time += task_elapsed_time
                tasklist_elapsed_time = round(tasklist_elapsed_time, 2)

                task_case = TaskReport(task_id=str(taskid), url=url, header=task_header, in_param=task_in_param,
                                       result=task_result, expect=task_expect, status=task_status,
                                       elapsed_time=task_elapsed_time, execute_time=task_execute_time,
                                       app_id=str(app_ver),
                                       page_id=str(pageid), case_id=str(caseid))
                task_case.save()
                tasklist = TaskList.objects.filter(task_id=taskid).update(case_count=ccount, pass_count=pcount,
                                                                          fail_count=fcount,
                                                                          elapsed_time=tasklist_elapsed_time,
                                                                          execute_time=task_execute_time)


            else:
                task_case = TaskReport(task_id=str(taskid), url=url, header=task_header, in_param=task_in_param,
                                       result=task_result, expect=task_expect, status=task_status,
                                       elapsed_time=task_elapsed_time, execute_time=task_execute_time,
                                       app_id=str(app_ver),
                                       page_id=str(pageid), case_id=str(caseid))
                task_case.save()

    tasklist = TaskList.objects.filter(task_id=taskid).update(case_count=ccount, pass_count=pcount,
                                                              fail_count=fcount,
                                                              elapsed_time=tasklist_elapsed_time,
                                                              execute_time=task_execute_time)
    extime = task_execute_time.strftime('%Y-%m-%d %H:%M:%S')
    tasklist_elapsed_time = round(tasklist_elapsed_time, 2)
    tasks = TaskReport.objects.filter(task_id=taskid)
    tasklist = TaskList.objects.get(task_id=taskid)
    context = {'tasks': tasks, 'tasklist': tasklist}
    static_html = "F:/NewApi/appapi/templates/"+taskid+".html"
    if not os.path.exists(static_html):
        content = render_to_string('template.html', context)
        with open(static_html, "w", encoding='utf-8') as static_file:
            static_file.write(content)


    return HttpResponse(json.dumps({
        "taskid": taskid,
        "ccount": ccount,
        "pcount": pcount,
        "fcount": fcount,

        "eltime": tasklist_elapsed_time,
        "extime": extime
    }, ensure_ascii=False))


def taskreport(request, id):

    return render(request,id+'.html')
