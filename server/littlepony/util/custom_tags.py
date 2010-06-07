"""
Simple module that wraps neccecary Django code to create custom template tags. Includes two flavors: custom tags that allow inner tags and content, and custom tags that do not. The do_custom_tag and do_simple_custom_tag respectfully. Both version support a simple syntax for passing plain text (non-dynamic) options.

Basic example of custom tag that allows inner tags:

from custom_tags import do_custom_tag, do_simple_custom_tag, do_inner, get_options

------------
templatetags
------------
@register.tag(name="tag-inner")
def do_my_inner(parser, token): 
    return do_inner(parser, token)

@register.tag(name="box")
def do_box(parser, token):
    return do_custom_tag(parser, token, "endbox", "app/tags/box.html")
    
--------
box.html
--------
{% load app %}
<div class="box {{tag_options.classes}}">
    {% tag-inner %}
    {{tag_options.extra_text}}
</div>

-----------------
sometemplate.html
-----------------
{% load app %}
{% box classes=foo bar|extra_text=something nice %}{{anything}}{% endbox %}
"""

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

def do_inner(parser, token):
    return InnerNode()

class InnerNode(template.Node):
    def __init__(self):
        self.rendered = ""

    def __repr__(self):
        return "<Inner node>"

    def render(self, context):
        return self.rendered

class CustomTagNode(template.Node):
    def __init__(self, nodelist, options, filename):
        self.nodelist = nodelist
        self.filename = filename
        self.options = options

    def __repr__(self):
        return "<CustomTagNode>"

    def render(self, context):
        (t, o) = template.loader.find_template(self.filename)
        nodelist = t.nodelist

        for node in nodelist:
            if type(node) == InnerNode:
                node.rendered = self.nodelist.render(context)

        context["tag_options"] = self.options
        return nodelist.render(context)

class SimpleCustomTagNode(template.Node):
    def __init__(self, options, filename):
        self.options = options
        self.filename = filename

    def __repr__(self):
        return "<SimpleCustom node>"

    def render(self, context):
        (t, o) = template.loader.find_template(self.filename)
        nodelist = t.nodelist

        context["tag_options"] = self.options
        return nodelist.render(context)


def get_options(token):
    split = " ".join(token.contents.split(" ")[1:]) # remove the tag name
    split = split.split("|") # split options on |

    options = {}
    for item in split:
        option = item.split('=')
        try:
            options[option[0]] = option[1]
        except:
            pass
    return options

def do_custom_tag(parser, token, endtag, filename):
    options = get_options(token)
    nodelist = parser.parse((endtag,))
    parser.delete_first_token()
    return CustomTagNode(nodelist, options, filename)

def do_simple_custom_tag(parser, token, filename):
    options = get_options(token)
    return SimpleCustomTagNode(options, filename)