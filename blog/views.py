from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View, generic
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from blog import serializers
from blog.classes import CreateRetrieveUpdateDestroy
from blog.forms import PostForm
from blog.models import Post
from blog.permissions import IsAuthor
from blog.serializers import ListPostSerializer, PostSerializer


class MainView(View):
    def get(self, request):
        return render(request, 'blog/main.html')


class UserLoginView(LoginView):
    template_name = 'registration/login.html'


class UserView(View):
    def get(self, request):
        return render(request, 'blog/user_info.html')


class UserLogoutView(LogoutView):
    template_name = 'blog/logout.html'


class UserListView(generic.ListView):
    model = User
    template_name = 'blog/user_list.html'
    context_object_name = 'user_list'


class UserDetailView(generic.DetailView):
    model = User
    template_name = 'blog/user_detail.html'
    context_object_name = 'user_detail'


class PostCreateView(View):
    def get(self, request):
        post_form = PostForm
        return render(request, 'blog/post_form.html', {'post_form': post_form})

    def post(self, request):
        post_form = PostForm(request.POST)
        post_form.author = request.user
        new_post = post_form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return HttpResponseRedirect(reverse('user-detail', args=[request.user.id]))


class UserList(generics.ListAPIView):
    """
    Users' list
    """
    queryset = User.objects.all()
    serializer_class = serializers.GetUserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    One user's info
    """
    queryset = User.objects.all()
    serializer_class = serializers.GetUserSerializer


class PostListView(generics.ListAPIView):
    """
    User's wall
    """
    serializer_class = ListPostSerializer[:500]
    paginator = Paginator(serializer_class, 10)

    def get_queryset(self):
        return Post.objects.filter(
            user_id=self.kwargs.get('pk')).select_related('user')


class PostView(CreateRetrieveUpdateDestroy):
    """
    Post's CRUD
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().select_related('user')
    serializer_class = PostSerializer
    permission_classes_by_action = {'get': [AllowAny],
                                    'update': [IsAuthor],
                                    'destroy': [IsAuthor]}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)