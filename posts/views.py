from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.urls import reverse

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post

User = get_user_model()


def index(request):
    posts = Post.objects.order_by('-pub_date')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = p.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = p.get_page(page_number)
    return render(request, 'group.html', context={'group': group, 'page': page})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render(request, 'new.html', context={'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.order_by('-pub_date')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = p.get_page(page_number)
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user)
    else:
        following = None
    return render(request, 'profile.html', context={'author': author,
                                                    'page': page, 'following': following})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=author, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post', username=username, post_id=post_id)
    comments = post.comments.order_by('-created')
    form = CommentForm()
    return render(request, 'post.html', context={'author': author, 'post': post, 'comments': comments,
                                                 'form': form})


def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=author)
    if request.user.username != username:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post', username=username, post_id=post_id)
    return render(request, 'edit.html', context={'form': form, 'post': post})


@login_required
def add_comment(request, username, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            author = get_object_or_404(User, username=username)
            post = get_object_or_404(Post, id=post_id, author=author)
            comment = form.save(commit=False)
            comment.author = author
            comment.post = post
            comment.save()
            return redirect('post', username=username, post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', context={'form': form})


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def follow_index(request):
    followings = Follow.objects.filter(user=request.user)
    posts = Post.objects.filter(author__following__in=followings).order_by('-pub_date')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = p.get_page(page_number)
    return render(request, 'follow.html', {'page': page})


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















