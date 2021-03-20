from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_object_or_404, redirect, render)
from django.views.generic import (DetailView, ListView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, Comment
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
User = get_user_model()


class PostsListView(ListView):
    queryset = Post.objects.all().order_by('-pub_date')
    template_name = 'index.html'
    paginate_by = 10


class GroupPostsView(ListView):
    paginate_by = 10
    template_name = 'group.html'

    def get_queryset(self):
        posts = Post.objects.filter(group__slug=self.kwargs['slug']).order_by('-pub_date')
        return posts


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'new.html'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProfileView(SingleObjectMixin, ListView):
    model = Post
    template_name = 'profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        print(request.GET)
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        return self.object.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.object
        is_subscribed = Follow.objects.filter(author=self.object, user=self.request.user)
        context['is_subscribed'] = is_subscribed
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return Post.objects.get(author__username=self.kwargs.get('username'), id=self.kwargs.get('id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-created')
        is_subscribed = Follow.objects.filter(author=self.object.author, user=self.request.user)
        context['is_subscribed'] = is_subscribed
        return context


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'edit.html'
    permission_required = 'posts.change_item'


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = get_object_or_404(Post, author__username=self.kwargs.get('username'),
                                             id=self.kwargs.get('id'))
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'username': self.kwargs.get('username'),
                                       'id': self.kwargs.get('id')})


class FollowPostsListView(ListView):
    template_name = 'follow.html'
    paginate_by = 10

    def get_queryset(self):
        followings = Follow.objects.filter(user=self.request.user).values_list('author_id')
        posts = Post.objects.filter(author__id__in=followings)
        return posts


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)














