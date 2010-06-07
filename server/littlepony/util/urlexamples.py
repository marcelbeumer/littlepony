def get_urlconf():
    from django.conf import settings
    from django.utils.importlib import import_module
    name = settings.ROOT_URLCONF
    if not name:
        raise Exception("could not find urlconf module name (%s)" % name)
    urlconf = import_module(name)
    return urlconf

def urlexample(*args, **kwargs):
    if len(args) == 0:
        return {}
    o = {
        'url' : args[0]
    }
    o.update(**kwargs)
    return o

def export_static():
    from django.test.client import Client
    c = Client()
    urlconf = get_urlconf()
    for example in urlconf.urlexamples:
        
        if example.get('noexport', False):
            continue
            
        url = example['url']
        description = ""
        if example.has_key('description'):
            description = example['description']
        
        request = c.get(url, follow=True)
        code = request.status_code
        response = request.content
        content_type = request['content-type']
        
        if code != 200:
            raise Exception("request to %s gave HTTP code %s instead of 200." % (url, code))
        
        if example.has_key('filename'):
            filename = example['filename']
        else:
            from django.template.defaultfilters import slugify
            ext = ".txt"
            if 'text/html' in content_type: ext = ".html"
            if description != "":
                filename = slugify(description) + ext
            else:
                filename = slugify(url)
        
        if not filename or filename == "":
            raise Exception("could not compose filename for url '%s'" % url)
            
        yield {'filename' : filename, 'response' : response, 'url' : url, 'description' : description, 'content_type' : content_type,}
        
def render_index(statics=None):
    statics = statics and statics or [s for s in export_static()]
    from django.conf import settings
    import os
    template_name = getattr(settings, 'EXPORTURLEXAMPLES_INDEX_TEMPLATE', False)
    if not template_name:
        raise Exception("could not render index, EXPORTURLEXAMPLES_INDEX_TEMPLATE not set properly.")
    from django.template import Context, loader, RequestContext, TemplateDoesNotExist
    try:
        t = loader.get_template(template_name)
    except TemplateDoesNotExist:
        raise Http404
    return t.render(Context({'statics' : statics}))
    