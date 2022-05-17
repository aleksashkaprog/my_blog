from django.contrib.auth.models import User
from django.urls import path
from .views import MainView, LoginView, LogoutView, UserListView, UserDetailView, PostCreateView, UserView
from drf_yasg import openapi

from . import views
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns


schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="Описание проекта",
        terms_of_services="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="alexandrsgrusina@gmail.com"),
        license=openapi.License(name='')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('blog/login', LoginView.as_view(), name='login'),
    path('blog/logout', LogoutView.as_view(), name='logout'),
    path('blog/users', UserListView.as_view(queryset=User.objects.all().order_by('-username')),
         name='user-list'),
    path('blog/user/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('blog/posts/create', PostCreateView.as_view(), name='post-create'),
    path('accounts/profile/', UserView.as_view(), name='user-info'),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('post/', views.PostView.as_view({'post': 'create'})),
    path('post/<int:pk>', views.PostView.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),
    path('posts/<int:pk>', views.PostListView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)