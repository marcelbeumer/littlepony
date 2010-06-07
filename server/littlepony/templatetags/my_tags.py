from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
from littlepony.util.custom_tags import do_custom_tag, do_simple_custom_tag, do_inner

@register.filter(name='replace_special_css_class')
@stringfilter
def replace_special_css_class(value):
    return value.replace('__special', 'notspecial')
