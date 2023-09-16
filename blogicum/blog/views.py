from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Post, Category, Comment
import datetime as dt
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .forms import PostForm, CommentForm, UserUpdateForm
from django.core.exceptions import PermissionDenied
from django.db.models import Count

User = get_user_model()


class PostListView(ListView):
    paginate_by = 10
    model = Post
    template_name = 'blog/index.html'

    def get_queryset(self):
        queryset = Post.objects.select_related('author')\
            .select_related('location').select_related('category').filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=dt.datetime.now(),
            ).annotate(comment_count=Count('comments')).order_by('-pub_date')
        return queryset


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10
    ordering = '-pub_date'

    def get_queryset(self):
        if self.kwargs['author'] != self.request.user.username:
            return Post.objects.select_related('author')\
                .select_related('location')\
                .select_related('category').filter(
                author__username=self.kwargs['author'],
                is_published=True,
                category__is_published=True,
                location__is_published=True,
                pub_date__lte=dt.datetime.now()
                ).order_by('-pub_date')\
                .annotate(comment_count=Count('comments'))
        else:
            return Post.objects.select_related('author')\
                .select_related('location')\
                .select_related('category').filter(
                author__username=self.kwargs['author'],
                ).order_by('-pub_date')\
                .annotate(comment_count=Count('comments'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = (
            get_object_or_404(User, username=self.kwargs['author'])
            )
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        object = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if object.author != self.request.user:
            return get_object_or_404(Post,
                                     pk=self.kwargs['post_id'],
                                     is_published=True,
                                     category__is_published=True,
                                     location__is_published=True,
                                     pub_date__lte=dt.datetime.now()
                                     )
        else:
            return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'

    def get_queryset(self):
        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug']
            )
        if category.is_published:
            queryset = Post.objects.select_related('author')\
                .select_related('location')\
                .select_related('category').filter(
                        is_published=True,
                        category__is_published=True,
                        pub_date__lte=dt.datetime.now(),
                        category__slug=self.kwargs['category_slug'],
            ).annotate(comment_count=Count('comments')).order_by('-pub_date')
            return queryset
        else:
            raise Http404
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = (
            get_object_or_404(Category, slug=self.kwargs['category_slug'])
            )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    article = None
    model = Comment
    form_class = CommentForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        print('Переопределяем form_valid()')
        form.instance.author = self.request.user
        form.instance.post = self.post_object
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.post_object.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('blog:edit_profile')

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'author': self.request.user.username})
