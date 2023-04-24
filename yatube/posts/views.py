from django.core.paginator import Paginator
from constants import OPTIMAL_NUMBER_OF_POSTS
from django.shortcuts import get_object_or_404, render, redirect
from .models import Group
from .models import Post
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import PostForm


User = get_user_model()


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, OPTIMAL_NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = (Post.objects.filter(group=group).order_by
             ('-pub_date')[:OPTIMAL_NUMBER_OF_POSTS])
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, OPTIMAL_NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author').all()
    page_number = request.GET.get('page')
    paginator = Paginator(posts, OPTIMAL_NUMBER_OF_POSTS)
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts': posts,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post
    }
    return render(request, template, context)


@login_required()
def post_create(request):
    template = 'posts/create.html'
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create.html'
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    form = PostForm(request.POST or None, instance=post)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    if form.is_valid():
        post = form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': is_edit,
        'post_id': post_id,
    }
    return render(request, template, context)
