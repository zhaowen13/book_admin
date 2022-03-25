from .models import Book, Branch, Borrow
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import validators




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')



class BranchSerializer(serializers.ModelSerializer):
    """书籍分类"""
    # 必传字段 UniqueValidator校验唯一性 
    branch_name = serializers.CharField(required=True,
                                       max_length=15,
                                       min_length=2,
                                       validators=[validators.UniqueValidator(queryset=Branch.objects.all(),message="分类已存在")]
                                       )    
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 设置日期格式化格式    
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 设置日期格式化格式                                                    
    class Meta:
        model = Branch
        fields = '__all__'

class BrancDeserializer(serializers.ModelSerializer):
    """书籍分类反序列化  加了别的表字段就要重写反序列化"""     
    class Meta:
        model = Branch
        fields = ('id','branch_name','branch_summary','is_delete','created_at','update_name','updated_at')


class BookDeserializer(serializers.ModelSerializer):
    """书籍信息反序列化  加了别的表字段就要重写反序列化"""     
    class Meta:
        model = Book
        fields  = ('id','branch_id','book_name','author','press','book_summary','is_delete','created_at','update_name','updated_at')

class BookSerializer(serializers.ModelSerializer):
    """书籍名称"""
    branch_name = serializers.CharField(source='branch_id.branch_name')   #在models中设置好branch_id指向哪个表
    # 必传字段 UniqueValidator校验唯一性
    book_name = serializers.CharField(required=True,
                                       max_length=15,
                                       min_length=2,
                                       validators=[validators.UniqueValidator(queryset=Book.objects.all(),message="书籍已存在")]
                                       )     
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 设置日期格式化格式    
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 设置日期格式化格式                                                  
    class Meta:
        model = Book
        # 不能用 '__all__' 会branch_id 变为branch
        fields = ('id','branch_name','branch_id','book_name','author','press','book_summary','is_delete','created_at','update_name','updated_at')

class BorrowSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 设置日期格式化格式    
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 设置日期格式化格式  
            
    class Meta:
        model = Borrow
        fields = ('id', 'vip_name', 'book_name', 'status', 'is_delete', 'created_at',
                  'update_name', 'updated_at')

class BorrowDeserializer(serializers.ModelSerializer):

    class Meta:
        model = Borrow
        fields = ('id', 'vip_name', 'book_name', 'status', 'is_delete', 'created_at',
                  'update_name', 'updated_at')
