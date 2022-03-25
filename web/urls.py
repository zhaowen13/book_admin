# from django.conf.urls import url, include
from django.urls import path, include,re_path
from rest_framework import routers
from my_web.views import BookViewSet,BranchViewSet,BorrowhViewSet,obtain_expiring_auth_token
from django.views.generic import TemplateView
from django.conf import settings
from django.views.static import serve
from django.contrib import admin

router = routers.DefaultRouter()
router.register('book', BookViewSet)
router.register('branch', BranchViewSet)
router.register('borrowh', BorrowhViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_expiring_auth_token, name='api-token'),
    path('admin/', admin.site.urls),
    re_path(r'^', TemplateView.as_view(template_name="index.html")),
    re_path(r'^static/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),
   
]

# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
# urlpatterns = [
#     url(r'^api/', include(router.urls)),
#     url(r'^api/login$', login),
#     url(r'^api-token-auth/', views.obtain_auth_token),
#     url(r'^admin/', admin.site.urls),
#     url(r'^', TemplateView.as_view(template_name="index.html")),
#     url(r'^static/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),
   
# ]