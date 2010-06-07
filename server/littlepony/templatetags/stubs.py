from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
from littlepony.util.custom_tags import do_custom_tag, do_simple_custom_tag, do_inner

@register.tag(name="tag-inner")
def do_my_inner(parser, token):
    return do_inner(parser, token)

@register.tag(name="xxx")
def do_xxx(parser, token):
    return do_simple_custom_tag(parser, token, "tags/stubs/dummy-simple.html")

@register.tag(name="startspecial")
def do_special(parser, token):
    return do_custom_tag(parser, token, "endspecial", "tags/stubs/dummy.html")

@register.filter(name='special')
def do_specialfilter(value):
    return value
