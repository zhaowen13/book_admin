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


class book(models.Model):
    book_name = models.CharField('书籍名称',unique=True, max_length=64)
    branch_id = models.IntegerField('分类ID', max_length=64)
    author = models.CharField('作者', max_length=64)
    press = models.CharField('出版社', max_length=64)
    book_summary = models.CharField('书籍简介', max_length=500)
    is_delete = models.BooleanField('逻辑删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_name = models.CharField('更新人', max_length=64)
    updated_at = models.DateTimeField('最后修改日期', auto_now=True)

    def __unicode__(self):
        return self.fundcode

    class Meta:
        db_table = "book"


class branch(models.Model):
    branch_name = models.CharField('分类名', unique=True, max_length=64)
    branch_summary = models.CharField('分类简介', max_length=500)
    is_delete = models.BooleanField('逻辑删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_name = models.CharField('更新人', max_length=64)
    updated_at = models.DateTimeField('最后修改日期', auto_now=True)

    def __unicode__(self):
        return self.fundcode

    class Meta:
        db_table = "branch"


class borrow(models.Model):
    vip_name = models.CharField('会员名称',unique=True, max_length=64)
    book_name = models.CharField('书籍名称', max_length=500)
    borrow_time = models.DateTimeField('借阅时间')
    end_time = models.DateTimeField('归还时间')
    status = models.BooleanField('借阅状态')
    is_delete = models.BooleanField('逻辑删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    update_name = models.CharField('更新人', max_length=64)
    updated_at = models.DateTimeField('最后修改日期', auto_now=True)

    def __unicode__(self):
        return self.fundcode

    class Meta:
        db_table = "borrow"






