import json
import datetime
from django.utils import datetime_safe

from django.db import models
from django.db.models.query import QuerySet
from django.core import serializers
from django.core.serializers import python as python_serializers

class PythonSerializer(python_serializers.Serializer):
    """
    Serializes a QuerySet to basic Python objects, resembling viewdata.
    """
    
    def __init__(self, extra=None):
        self.extra = extra

    def end_object(self, obj):
        for key in self.extra:
            if str(type(obj)) == str(key):
                for att in self.extra[key]:
                    self._current[att] = getattr(obj, att)
        self.objects.append(self._current)
        self._current = None

class ViewDataEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    
    def __init__(self, *args, **kwargs):
        if kwargs.has_key('extra'): 
            self.extra = kwargs['extra']
            del kwargs['extra']
        super(ViewDataEncoder, self).__init__(*args, **kwargs)
    
    def default(self, obj):
        if isinstance(obj, QuerySet):
            s = PythonSerializer(self.extra)
            s.serialize(obj)
            return s.getvalue()
        elif isinstance(obj, datetime.datetime):s
            d = datetime_safe.new_datetime(obj)
            return d.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
        elif isinstance(obj, datetime.date):
            d = datetime_safe.new_date(obj)
            return d.strftime(self.DATE_FORMAT)
        elif isinstance(obj, datetime.time):
            return obj.strftime(self.TIME_FORMAT)
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        else:
            return super(DjangoJSONEncoder, self).default(obj)
        d = json.JSONEncoder.default(self, obj)
        return d
        
def dump_viewdata(viewdata, extra=None):
    return json.dumps(viewdata, cls=ViewDataEncoder, indent=10, extra=extra)

def load_viewdata(json):
    return json.loads(json)
