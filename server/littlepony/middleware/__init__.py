import urllib, urllib2
from django.http import HttpResponse, HttpResponseServerError

def validate_html(html):
    """
    Validates the html string using a commandline script called validate_html5.
    TODO: make sure the script can be run from anywhere - now it assumes a certain rootpath.
    
    returns [bool, message]
    """
    import os
    from subprocess import Popen, PIPE, STDOUT
    path = os.path.abspath(os.path.dirname(__file__))
    p = Popen([os.path.join(path, 'html5check.py'), '-h'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout = p.communicate(input=html)[0]
    return [not 'There were errors.' in stdout, stdout]
    
def message_to_html(text):
    """
    Converts the commandline output of validate_html5.py to basic HTML with paragraphs.
    """
    text = "<p>" + text
    text = text.replace("\n\n", "</p>")
    text = text + "<p>"
    return text

class ValidateHTML5(object):
    """
    Middleware that checks every response with Content-Type html if it is valid HTML5.
    Add ValidateHTML5 to your middleware classes to enable.
    """
    def process_response(self, request, response):
        validate = request.GET.get('validate', False)
        if validate == False:
            return response
        if not self._should_validate(request, response):
            return response 
            
        valid, message = validate_html(response.content)
        return HttpResponse(message_to_html(message))
    
    def _should_validate(self, request, response):
        return 'html' in response['Content-Type']