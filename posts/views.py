from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PostForm
from .models import Group, Post


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    return render(request, 'index.html', {'posts': posts})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:12]
    return render(request, 'group.html', context={'group': group, 'posts': posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # post = form.save(commit=False)
            # post.author = request.user
            # post.save()
            data = form.cleaned_data
            Post.objects.create(text=data['text'], group=data['group'], author=request.user)
            return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render(request, 'new.html', context={'form': form})
