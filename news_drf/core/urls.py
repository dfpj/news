from django.contrib import admin
from django.urls import path,include

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework import routers

from news.api_views import NewsViewSet,AuthorViewSet,TagViewSet
from accounts.api_views import UserViewSet,send_code_to_email,check_verify_code, ProfileViewSet
from comment.api_views import CommentViewSet


router = routers.SimpleRouter()
router.register('user',UserViewSet,basename='user')
router.register('profile',ProfileViewSet,basename='profile')
router.register('news',NewsViewSet,basename='news')
router.register('author',AuthorViewSet,basename='author')
router.register('tag',TagViewSet,basename='tag')
router.register('comment',CommentViewSet,basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/check_code/', check_verify_code),
    path('user/send_code/<int:id>/', send_code_to_email),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
