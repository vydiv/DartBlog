from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import CommentForm
from .models import Post, Category, Tag, Comment
from django.db.models import F


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Classic Blog Design'
        return context


class PostByCategory(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostByTag(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))

        return context


class GetPost(FormMixin, DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        # post = Post.objects.get(slug=self.kwargs['slug'])
        # comments = Comment.objects.filter(post=post)
        # context = {
        #     "post": post,
        #     "comments": comments,
        #     # "form": form,
        # }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        post = Post.objects.get(slug=self.kwargs['slug'])

        comment = Comment(
            author=form.cleaned_data["author"],
            body=form.cleaned_data["body"],
            email=form.cleaned_data["email"],
            post=post
        )
        comment.save()
        return HttpResponseRedirect(self.request.path_info)


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s = {self.request.GET.get('s')} &"
        return context

# def index(request):
#     return render(request, 'blog/index.html')
#
#
# def get_category(request, slug):
#     return render(request, 'blog/category.html')
#
#
# def get_post(request, slug):
#     return render(request, 'blog/category.html')
