from littlepony.util.views import *

def page(request, template, viewdata={}):
    return render_to_response(request, '%s.html' % template, viewdata)

def json_page(request, template="", jsonfile=""):
    data = load_json('%s.json' % jsonfile)
    return page(request, template=template, viewdata=data)

def products(request):
    data = load_json('products.json')
    print len(data)
    return page(request, template="products", viewdata=data)
