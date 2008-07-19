import os
import mimetypes

mimetypes.add_type('text/html', '.stx')
mimetypes.add_type('application/pdf', '.pdf')

from zope.component import getMultiAdapter
from zope.structuredtext import stx2html

from webob import Response

from repoze.bfg.interfaces import IView

def file_view(context, request):
    dirname, filename = os.path.split(context.path)
    name, ext = os.path.splitext(filename)
    result = getMultiAdapter((context, request), IView, name=ext)
    return result

def directory_view(context, request):
    defaults = ('index.html', 'index.stx')
    for name in defaults:
        try:
            index = context[name]
        except KeyError:
            continue
        return file_view(index, request)
    response = Response('No default view for %s' % context.path)
    response.content_type = 'text/plain'
    return response
        
def structured_text_view(context, request):
    """ Filesystem-based STX view
    """
    result = stx2html(context.source)
    response = Response(result)
    response.content_type = 'text/html'
    return response

def raw_view(context, request):
    """ Just return the source raw.
    """
    response = Response(context.source)
    dirname, filename = os.path.split(context.path)
    name, ext = os.path.splitext(filename)
    mt, encoding = mimetypes.guess_type(filename)
    response.content_type = mt or 'text/plain'
    return response
