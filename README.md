# DartBlog

Функционал блога: 

- [Главная страница](#index) 
- [Вывод постов по категории](#category)
- [Детальный вид поста](#details)
- [Поиск по заголовку поста](#title)
- [Вывод тегов](#tag)
- [Вывод популярных постов](#popular)
- [Добавление комментариев к посту](#comments)
- [Форма контакты](#contact) 


## <a name="index">Главная страница</a>
Шапка сайта на котором выводяся существующие категории.
![image](https://user-images.githubusercontent.com/11966417/183940678-d94c2c9e-c2e2-4058-90ea-412d189adfc1.png)
Самый <a name="popular">просматриваемый пост</a> , реализовано с помощью пользовательского тега
![image](https://user-images.githubusercontent.com/11966417/183941538-29575347-ab6c-4a53-907a-a1cff07cb411.png)

```python
from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/popular_post_tpl.html')
def get_popular_post(cnt=1):
    post_pop = Post.objects.order_by('-views')[:cnt]
    print({'post_pop': post_pop})
    return {'post_pop': post_pop}
```
Отображение существующих постов со встроенной пагинацией 
![image](https://user-images.githubusercontent.com/11966417/183941757-ca9a9902-4040-4841-8784-f23d506fe3d1.png)
```html
{% if page_obj.has_other_pages %}
    <div class="pegination">
        <div class="nav-links">

            {% for p in page_obj.paginator.page_range %}
            {% if page_obj.number == p %}
            <span class="page-numbers current">{{ p }}</span>
            {% elif p > page_obj.number|add:-3 and p < page_obj.number|add:3 %}
            <a class="page-numbers" href="?page={{ p }}">{{ p }}</a>
            {% endif %}
            {% endfor %}

            {% if page_obj.has_next %}
            <a class="page-numbers" href="?page={{ page_obj.next_page_number }}"><i class="fa fa-angle-right"
                                                                                    aria-hidden="true"></i></a>
            {% endif %}
        </div>
    </div>
    {% endif %}
```
Подвал сайта с кликабельными категориями постов 
![image](https://user-images.githubusercontent.com/11966417/183942407-5ea9308c-ce2a-4251-b631-44decc884984.png)


## <a name="category">Вывод постов по категории</a> 
По клику на шапке или подвале мы попадаем на отображение записей по категории 
![image](https://user-images.githubusercontent.com/11966417/183942725-4fc42393-a0ee-436b-bb62-8ad1aa3e6cac.png)

```python
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
```

## <a name="details">Детальный вид поста</a>
![image](https://user-images.githubusercontent.com/11966417/183943305-a7b07e2d-4bbe-486f-84ce-fd14ea3d4308.png)
На этой странице пристутствует: 
### <a name="title">Поиск по заголовку поста</a>
![image](https://user-images.githubusercontent.com/11966417/183944154-cafb9a1c-4dc8-4edd-a698-adccc1baf759.png)

### <a name="tag">Вывод тегов</a>
![image](https://user-images.githubusercontent.com/11966417/183944116-3768d160-5c56-4f55-b101-52af5fb68600.png)

### <a name="comments">Добавление комментариев к посту</a> 
![image](https://user-images.githubusercontent.com/11966417/183944003-e2fc948e-4f51-4d91-ae84-3a1a264d1595.png)

```python
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
```
## <a name="contact">Форма контакты</a> с подключенной капчей при отправке 
![image](https://user-images.githubusercontent.com/11966417/183945136-f27891c5-dd82-41be-99e1-9db047558ef8.png)
```python
class ContactForm(forms.Form):
    user_name = forms.CharField(label='Имя',
                                widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Ваше имя"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Введите существующий email"
        }))
    content = forms.CharField(label='Текст', widget=forms.Textarea(
        attrs={'class': 'form-control', "rows": 5, "placeholder": "Сообщение..."}))
    captcha = CaptchaField()
```
