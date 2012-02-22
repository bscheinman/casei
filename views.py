from casei.forms import SignupForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def render_with_request_context(request, page, context):
    return render_to_response(page, RequestContext(request, context))


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return render_with_request_context(request, 'signup.html', { 'form':SignupForm() })


def do_signup(request):
    if request.user.is_authenticated() or request.method != 'POST':
        return HttpResponseRedirect('/')
    form = SignupForm(request.POST)
    if not form.is_valid():
        return render_with_request_context(request, 'signup.html', { 'form':form })
    data = form.cleaned_data
    user = User.objects.create_user(data['username'], data['email'], data['password'])
    send_verification_email(user.email, user.profile.verification_id)

    return HttpResponseRedirect('/signup_thanks/')


def signup_thanks(request):
    return render_with_request_context(request, 'signup_thanks.html', { })



def do_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/ncaa/')
