from django.shortcuts import render_to_response
from django.template import RequestContext

def render_with_request_context(request, page, context):
    return render_to_response(page, RequestContext(request, context))
