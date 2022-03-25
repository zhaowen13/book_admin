import datetime
import pytz
from django.conf import settings
from rest_framework import status
from .models import Book, Branch, Borrow
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import BookSerializer, UserSerializer, BranchSerializer,BrancDeserializer,BorrowSerializer,BorrowDeserializer,BookDeserializer

 
EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 60*60*60*12)
 
class ObtainExpiringAuthToken(ObtainAuthToken):
    """Create user token"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.validated_data['user'])
 
            time_now = datetime.datetime.now()
            now=(time_now - datetime.timedelta(minutes=EXPIRE_MINUTES)).replace(tzinfo=pytz.timezone('UTC'))   #转换成UTC时区
            if created or token.created < now:
                # Update the created time of the token to keep it valid
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = time_now
                token.save()
 
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()


class BookViewSet(viewsets.ModelViewSet):
    """书籍管理"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('book_name',)

    # def list(self,request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     branch_list=Branch.objects.all()
    #     branch_list=BranchSerializer(branch_list,many=True)
    #     for data in response.data:
    #         for br in branch_list.data:
    #             if data['branch_id'] == br['id']:
    #                 data.update({"branch_name":br['branch_name']})
    #     return Response(response.data)


    def create(self, request):
        request.data.update({"update_name": request.user.username})
        serializer = BookDeserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        request.data.update({"update_name": request.user.username})
        instance = self.get_object()
        serializer = BookDeserializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class BranchViewSet(viewsets.ModelViewSet):
    """
    分类管理
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('branch_name',)

    def create(self, request):
        request.data.update({"update_name": request.user.username})
        serializer = BrancDeserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        request.data.update({"update_name": request.user.username})
        instance = self.get_object()
        serializer = BrancDeserializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            return super(BranchViewSet, self).destroy(request, *args, **kwargs)
        except Exception:
            return Response("该分类下有书籍不能删除",status=404)


class BorrowhViewSet(viewsets.ModelViewSet):
    """
    借书管理
    """
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    filter_backends = (DjangoFilterBackend,)
    # search_fields = ('name','fundcode')
    filter_fields = ('book_name',)

    def create(self, request):
        request.data.update(
            {"update_name": request.user.username, "status": 1})
        serializer = BorrowDeserializer(data=request.data)
        list = Borrow.objects.filter(
            book_name=request.data['book_name'], status=1)
        if serializer.is_valid():
            if list.exists():
                return Response("该书已经借出", status=404)
            else:
                serializer.save()
                return Response({"status": 2000, "message": "添加成功"})
        return Response("添加失败", status=404)

    def update(self, request, pk=None):
        request.data.update(
            {"update_name": request.user.username, "status": 0})
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        list = Borrow.objects.filter(
            book_name=request.data['book_name'], status=0)
        if list.exists():
            return Response("该书已经还了", status=404)
        else:
            self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
