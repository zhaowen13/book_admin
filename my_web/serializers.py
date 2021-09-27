from .models import book, branch, borrow
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import book
from rest_framework import validators


class BookSerializer(serializers.HyperlinkedModelSerializer):
        # 必传字段 UniqueValidator校验唯一性
    book_name = serializers.CharField(required=True,
                                       max_length=15,
                                       min_length=2,
                                       validators=[validators.UniqueValidator(queryset=book.objects.all(),message="书籍已存在")]
                                       )
    class Meta:
        model = book
        fields = ('id', 'book_name', 'branch_id', 'author', 'press', 'book_summary', 'is_delete', 'created_at',
                  'update_name', 'updated_at')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class BranchSerializer(serializers.HyperlinkedModelSerializer):
    """序列化商品models"""

    # 必传字段 UniqueValidator校验唯一性
    branch_name = serializers.CharField(required=True,
                                       max_length=15,
                                       min_length=2,
                                       validators=[validators.UniqueValidator(queryset=branch.objects.all(),message="分类已存在")]
                                       )
    class Meta:
        model = branch
        fields = ('id', 'branch_name', 'branch_summary', 'is_delete', 'created_at',
                  'update_name', 'updated_at')



class BorrowSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = borrow
        fields = ('id', 'vip_name', 'book_name', 'borrow_time', 'end_time', 'status', 'is_delete', 'created_at',
                  'update_name', 'updated_at')
