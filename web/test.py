序列化文件
# -*- coding: utf-8 -*-
# @Time    : 2020/4/11 13:15
# @Author  : Bc

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from student.models import Student


# 自定义校验器，先执行，再执行内部自定义校验器
def is_unique_sno(sno):
    if "95" not in sno:
        raise serializers.ValidationError('学号是否包含95')


class StudentSerializer(serializers.Serializer):
    """ 创建序列化器类 """
    # 需要输出哪些字段，就定义哪些字段，默认为即进行序列化输出和反序列化输入
    # read_only=True： 只进行序列化输出，write_only=True： 只做反序列化输入
    GENDER_CHOICES = (('男', '男'), ('女', '女'))
    sno = serializers.CharField(label="SNo",
                                validators=[UniqueValidator(queryset=Student.objects.all(), message="学号不能重复"),
                                            is_unique_sno])  # 学号，唯一约束,并且包含95
    name = serializers.CharField(label="SName", max_length=100)  # 姓名
    gender = serializers.ChoiceField(label="Gender", choices=GENDER_CHOICES)  # 性别，选项选择
    mobile = serializers.CharField(label="Mobile", max_length=100)  # 手机号码，
    birthday = serializers.DateField(label="Birthday", read_only=True)  # 出生日期，只读，不需要填写
    email = serializers.CharField(label="Email", max_length=100, allow_blank=True, allow_null=True, default='')  # 邮箱地址
    address = serializers.CharField(label="Address", allow_null=True, allow_blank=True, default='',
                                    max_length=200)  # 家庭住址
    image = serializers.CharField(label="Image", read_only=True, max_length=200)  # 照片

    # 单字段校验
    def validate_sno(self, value):
        # startswith()： 以某某开头，endswith()： 以某某结尾
        if not value.startswith('95'):
            raise serializers.ValidationError('学号必须以95开头')
        # 内部校验成功后，必须返回
        return value

    # 多字段联合校验
    def validate(self, attrs):
        if '138' not in attrs['mobile'] and '张' not in attrs['name']:
            raise serializers.ValidationError('电话号码必须包含138,或者学生姓张')
        # 必须返回
        return attrs

    # 创建
    def create(self, validated_data):
        student_cls = Student.objects.create(**validated_data)
        return student_cls

    # 修改
    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.sno = validated_data['sno']
        instance.mobile = validated_data['mobile']
        instance.save()
        return instance

#2.类视图
# -*- coding: UTF-8 -*-
from django.http.response import JsonResponse, Http404
from django.views import View
from student.models import Student
from student.serializers import StudentSerializer
import json


class StudentsView(View):
    """ 学生类视图 """

    def get(self, request):
        """ 获取所有的学生数据 """
        query_set = Student.objects.all()
        # 序列化
        serializer = StudentSerializer(instance=query_set, many=True)
        return JsonResponse({"code": "200", "msg": "查询成功", "data": serializer.data}, safe=False)

    def post(self, request):
        """ 新增某学号数据 """
        request_data = request.body.decode('utf-8')
        python_dict = json.loads(request_data, encoding='utf-8')
        # 反序列化
        serializer = StudentSerializer(data=python_dict)
        try:
            # 反序列化验证
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse({"msg": "添加失败", "error": serializer.errors}, safe=False)
        # 序列化创建数据，保存
        serializer.save()
        return JsonResponse({"code": "201", "msg": "添加成功", "data": serializer.data}, safe=False)


class StudentDetail(View):

    def check_pk(self, pk):
        """ 验证是否存在学号 """
        try:
            return Student.objects.get(sno=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ 获取某学号的数据 """
        student_cls = self.check_pk(pk=pk)
        # 序列化
        serializer = StudentSerializer(instance=student_cls)
        return JsonResponse({"code": "200", "msg": "查询成功", "data": serializer.data}, safe=False)

    def put(self, request, pk):
        """ 修改某学号的数据 """
        student_cls = self.check_pk(pk=pk)
        # 获取前端数据
        request_data = request.body.decode('utf-8')
        python_dict = json.loads(request_data, encoding='utf-8')
        # 反序列化
        serializer = StudentSerializer(instance=student_cls, data=python_dict)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse({"msg": "修改失败", "error": serializer.errors}, safe=False)
        # 序列化修改，保存
        serializer.save()
        return JsonResponse({"code": "201", "msg": "修改成功", "data": serializer.data}, safe=False)

    def delete(self, request, pk):
        """ 删除某学号的数据 """
        student_cls = self.check_pk(pk=pk)
        # 删除
        student_cls.delete()
        return JsonResponse({"code": "201", "msg": "删除成功"}, safe=False)


#3.路由系统
  #  1.主路由
from django.contrib import admin
from django.urls import path, include


    urlpatterns = [

        path('admin/', admin.site.urls),

        path('', include('student.urls')),

    ]


    #2.子路由

from django.urls import path

from student import views



    urlpatterns = [

        path('students/', views.StudentsView.as_view()),

        path('students/<int:pk>/', views.StudentDetail.as_view()),

    ]

