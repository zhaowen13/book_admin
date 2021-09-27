from .models import book, branch, borrow
# from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookSerializer, UserSerializer, BranchSerializer, BorrowSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


class BookViewSet(viewsets.ModelViewSet):
    """
    书籍管理
    """
    queryset = book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('book_name',)

    def create(self, request):
        request.data.update({"update_name":request.user.username})
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        return Response(serializer.data)
        
    def update(self, request,pk=None):
        request.data.update({"update_name":request.user.username})
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class BranchViewSet(viewsets.ModelViewSet):
    """
    分类管理
    """
    queryset = branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('branch_name',)

    def create(self, request):
        request.data.update({"update_name":request.user.username})
        serializer = BranchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

      

    def update(self, request,pk=None):
        request.data.update({"update_name":request.user.username})
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

class BorrowhViewSet(viewsets.ModelViewSet):
    """
    借书管理
    """
    queryset = borrow.objects.all()
    serializer_class = BorrowSerializer
    filter_backends = (DjangoFilterBackend,)
    # search_fields = ('name','fundcode')
    filter_fields = ('vip_name',)

    def create(self, request):
        request.data.update({"update_name":request.user.username})
        serializer = BorrowSerializer(data=request.data)
        list=borrow.objects.filter(book_name=request.data['book_name'])
        if serializer.is_valid():
            if list.exists():
                return Response({"status":5001,"message": "该书已经借出"})
            else:
                serializer.save()
                return Response({"status":2000,"message": "添加成功"})
        return Response({"status":5000,"message": "添加失败"})


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
