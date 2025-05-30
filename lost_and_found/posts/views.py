from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import LostItemPost, Comment
from .forms import LostItemPostForm, CommentForm

# 홈 페이지 - 분실물 게시글 목록
def home(request):
    posts = LostItemPost.objects.all().order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})

# 게시글 상세보기
def post_detail(request, post_id):
    post = get_object_or_404(LostItemPost, pk=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

# 게시글 작성
def create_post(request):
    if request.method == 'POST':
        post_form = LostItemPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        post_form = LostItemPostForm()

    return render(request, 'posts/create_post.html', {'post_form': post_form})

# 로그인
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'posts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'posts/login.html')

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('home')
