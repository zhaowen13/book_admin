# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

'''
@File    :   models.py
@Time    :   2021/07/07 15:47:15
@Author  :   zhaowen
@Version :   1.0
@Desc    :   None
'''

class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    branch_name = models.CharField('分类名', unique=True, max_length=64)
    branch_summary = models.CharField('分类简介', max_length=500)
    is_delete = models.BooleanField('逻辑删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_name = models.CharField('更新人', max_length=64)
    updated_at = models.DateTimeField('最后修改日期', auto_now=True)

    def __str__(self):
        return self.branch_name

    class Meta:
        db_table = "branch"

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    book_name = models.CharField('书籍名称',unique=True, max_length=64)
    branch_id = models.ForeignKey(Branch,db_column='branch_id',on_delete=models.SET_NULL,null=True, verbose_name='分类')
    author = models.CharField('作者', max_length=64)
    press = models.CharField('出版社', max_length=64)
    book_summary = models.CharField('书籍简介', max_length=500)
    is_delete = models.BooleanField('逻辑删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_name = models.CharField('更新人', max_length=64)
    updated_at = models.DateTimeField('最后修改日期', auto_now=True)

    def __str__(self):
        return self.book_name

    class Meta:
        db_table = "book"



class Borrow(models.Model):
    id = models.AutoField(primary_key=True)
    vip_name = models.CharField('会员名称', max_length=64)
    book_name = models.CharField('书籍名称', max_length=500)
    created_at = models.DateTimeField('借阅时间',auto_now_add=True)
    updated_at = models.DateTimeField('归还时间',auto_now=True)
    status = models.BooleanField('借阅状态')
    is_delete = models.BooleanField('逻辑删除', default=False)
    update_name = models.CharField('更新人', max_length=64)
    

    def __str__(self):
        return self.vip_name

    class Meta:
        db_table = "borrow"






