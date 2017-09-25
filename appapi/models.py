from django.db import models
import django.utils.timezone as timezone
# Create your models here.
class Interface(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    summary = models.CharField(max_length=100)
    url = models.TextField(blank=True, null=True)
    case_count = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    elapsed_time =models.TextField(blank=True, null=True)
    create_time = models.DateTimeField('保存日期',auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True)
    execute_time = models.DateTimeField(blank=True, null=True)
    app = models.ForeignKey('App')
    page = models.ForeignKey('AppPage')

    def __str__(self):
        return self.name
    class Meta:
        db_table = 't_api'

class ApiCase(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey('Interface')
    name = models.CharField(max_length=100,null=True)
    header = models.TextField(blank=True, null=True)
    in_param = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    expect = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    elapsed_time = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField('保存日期',auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True)
    execute_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 't_api_case'

class App(models.Model):
    id = models.AutoField(primary_key=True)
    app_id=models.IntegerField(null=True)
    app_name = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField('保存日期', auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.app_name
    class Meta:
        db_table = 't_app'

class AppPage(models.Model):
    id = models.AutoField(primary_key=True)
    app=models.ForeignKey('App')
    page_id = models.IntegerField(null=True)
    page_name = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField('保存日期', auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.page_name
    class Meta:
        db_table = 't_app_page'

class TaskList(models.Model):
    id = models.AutoField(primary_key=True)
    task_id=models.CharField(max_length=20)
    task_name = models.CharField(max_length=100, null=True)
    case_count = models.TextField(blank=True, null=True)
    pass_count = models.TextField(blank=True, null=True)
    fail_count = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField('保存日期', auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True)
    execute_time = models.DateTimeField(blank=True, null=True)
    elapsed_time = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.task_id
    class Meta:
        db_table = 't_task_list'

class TaskReport(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=20)
    app=models.ForeignKey('App')
    page = models.ForeignKey('AppPage')
    case = models.ForeignKey('ApiCase')
    url = models.TextField(blank=True, null=True)
    header = models.TextField(blank=True, null=True)
    in_param = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    expect = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    elapsed_time = models.TextField(blank=True, null=True)
    execute_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.task_id
    class Meta:
        db_table = 't_task_report'

