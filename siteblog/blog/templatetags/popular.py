from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/popular_post_tpl.html')
def get_popular_post(cnt=1):
    post_pop = Post.objects.order_by('-views')[:cnt]
    print({'post_pop': post_pop})
    return {'post_pop': post_pop}



