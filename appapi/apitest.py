
from sqlalchemy import Column, String, create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, func
from appapi.utils import *
import time, datetime
import random

Base = declarative_base()


class Interface(Base):
    __tablename__ = "t_api"

    id = Column(String(20), primary_key=True, autoincrement=True)
    name = Column(String(100))
    summary = Column(String(100))
    url = Column(String(2000))
    case_count = Column(String(100))
    status = Column(String(2000))
    elapsed_time = Column(String(20))
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    execute_time = Column(DateTime)
    app_id = Column(String(20))
    page_id = Column(String(20))


class ApiCase(Base):
    __tablename__ = "t_api_case"

    id = Column(String(20), primary_key=True, autoincrement=True)
    api_id = Column(String(20))
    name = Column(String(100))
    header = Column(String(2000))
    in_param = Column(String(2000))
    result = Column(String(2000))
    expect = Column(String(2000))
    status = Column(String(2000))
    elapsed_time = Column(String(20))
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    execute_time = Column(DateTime)


class App(Base):
    __tablename__ = "t_app"

    id = Column(String(20), primary_key=True, autoincrement=True)
    app_id = Column(String(20))
    app_name = Column(String(20))
    create_time = Column(DateTime)
    update_time = Column(DateTime)


class AppPage(Base):
    __tablename__ = "t_app_page"

    id = Column(String(20), primary_key=True, autoincrement=True)
    app = Column(String, ForeignKey('app.id'))
    page_id = Column(String(20))
    page_name = Column(String(20))
    create_time = Column(DateTime)
    update_time = Column(DateTime)


class TaskList(Base):
    __tablename__ = "t_task_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(20))
    task_name = Column(String(100))
    case_count = Column(String(20))
    pass_count = Column(String(20))
    fail_count = Column(String(20))
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime)
    execute_time = Column(DateTime)
    elapsed_time = Column(String(20))


class TaskReport(Base):
    __tablename__ = "t_task_report"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(20))
    app_id = Column(String(20))
    page_id = Column(String(20))
    case_id = Column(String(20))
    url = Column(String(100))
    header = Column(String(2000))
    in_param = Column(String(2000))
    result = Column(String(2000))
    expect = Column(String(2000))
    status = Column(String(2000))
    elapsed_time = Column(String(100))
    execute_time = Column(DateTime)


DB_CONNECT_STRING = 'mysql+pymysql://root:123456@localhost/zallsat?charset=utf8'
engine = create_engine(DB_CONNECT_STRING)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()


def add_task():
    taskid = str(int(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))) + str(random.randint(0, 99))
    name = taskid
    casecount = 0
    passcount = 0
    failcount = 0
    estime = 0
    task = TaskList(task_name=name, task_id=taskid, case_count=casecount, pass_count=passcount,
                    fail_count=failcount, elapsed_time=estime)
    session.add(task)

    session.commit()

    return taskid


def run_task(taskid):
    apis = session.query(Interface)
    print(apis)
    pcount = 0
    fcount = 0
    ccount = 0
    tasklist_elapsed_time = 0


    for api in apis:

        app_ver = api.app_id
        pageid = api.page_id
        id = api.id

        url = api.url

        if app_ver == 1:
            zoken = user_token()
        else:
            zoken = car_token()

        api_cases = session.query(ApiCase).filter(ApiCase.api_id==api.id).all()
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
                session.add(task_case)
                session.commit()
                # tasklist = TaskList.objects.filter(task_id=taskid).update(case_count=ccount, pass_count=pcount,
                #                                                           fail_count=fcount,
                #                                                           elapsed_time=tasklist_elapsed_time,
                #                                                           execute_time=task_execute_time)


            else:
                task_case = TaskReport(task_id=str(taskid), url=url, header=task_header, in_param=task_in_param,
                                       result=task_result, expect=task_expect, status=task_status,
                                       elapsed_time=task_elapsed_time, execute_time=task_execute_time,
                                       app_id=str(app_ver),
                                       page_id=str(pageid), case_id=str(caseid))
                session.add(task_case)
                session.commit()

    # tasklist = TaskList.objects.filter(task_id=taskid).update(case_count=ccount, pass_count=pcount,
    #                                                           fail_count=fcount,
    #                                                           elapsed_time=tasklist_elapsed_time,
    #                                                           execute_time=task_execute_time)
    extime = task_execute_time.strftime('%Y-%m-%d %H:%M:%S')
    tasklist_elapsed_time = round(tasklist_elapsed_time, 2)

    return task_case


session.close()

if __name__ == "__main__":
    # taskid=add_task()
    run_task('2017081517210573')
