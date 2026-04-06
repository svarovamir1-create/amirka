from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Post

# ------------------------
# Список публикаций
# ------------------------
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='published')


# ------------------------
# Детальная страница
# ------------------------
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


# ------------------------
# Создание публикации
# ------------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'short_description', 'content', 'image', 'status']
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# ------------------------
# Редактирование публикации
# ------------------------
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'short_description', 'content', 'image', 'status']
    template_name = 'posts/post_form.html'

    def test_func(self):
        post = self.get_object()
        # Admin может всё, автор может свои посты
        return self.request.user.is_superuser or post.author == self.request.user


# ------------------------
# Удаление публикации
# ------------------------
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:list')

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_superuser or post.author == self.request.user


# ------------------------
# Лайк через fetch
# ------------------------
@login_required
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return JsonResponse({'likes': post.likes.count(), 'liked': liked})