from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import Context, loader, RequestContext, TemplateDoesNotExist
from django.template.loader import add_to_builtins
from django.core import urlresolvers
from django.core.urlresolvers import NoReverseMatch

def get_template(name):
    try:
        t = loader.get_template(name)
    except TemplateDoesNotExist:
        raise Http404
    return t
    
def load_json(jsonfile):
    from django.conf import settings
    import os, json
    path = getattr(settings, 'VIEWDATA_PATH', False)
    if not path: raise Exception("settings.VIEWDATA_PATH not set")
    f = open(os.path.join(path, jsonfile), 'r')
    data = json.loads(f.read())
    f.close()
    return data
    
def render_to_response(request, template, viewdata={}):
    t = get_template(template)
    return HttpResponse(t.render(RequestContext(request, viewdata)))
    
def index(request):
    from urlexamples import get_urlconf
    urlconf = get_urlconf()
    viewdata = {'urlexamples' : urlconf.urlexamples}
    return render_to_response(request, "builtin/index.html", viewdata=viewdata)

# patch Django url reverse
_django_reverse = None
def _reverse(*args, **kwargs):
    try:
        url = _django_reverse(*args, **kwargs)
    except NoReverseMatch:
        url = "NoReverseMatch"
    return url
def _patch_reverse():
    global _django_reverse
    if urlresolvers.reverse is not _reverse:
        _django_reverse = urlresolvers.reverse
        urlresolvers.reverse = _reverse
_patch_reverse()

add_to_builtins('littlepony.templatetags.stubs')
