from casei.ncaacards.models import 
from casei.views import render_with_request_context

def home(request):
    return render_with_request_context(request, 'cards_home.html', { })
