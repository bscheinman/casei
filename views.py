from casei.forms import LoginForm, SignupForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def render_with_request_context(request, page, context):
    return render_to_response(page, RequestContext(request, context))


def login(request):
    if request.user.is_authenticated() or request.method != 'POST':
        return HttpResponseRedirect('/')
    error = ''
    form = LoginForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            profile = UserProfile.objects.get(user=user)
            if not user.has_perm('auth.can_login'):
                error = 'User is not verified'
            elif not user.is_active:
                error = 'Your account has been disabled.  Please contact site administrators.'
            else:
                login(request, user)
        else:
            error = 'Invalid username or password'
    else:
        error = 'Please enter a valid username and password'
    if error:
        return render_with_request_context(request, 'home.html', { 'error':error })
    return HttpResponseRedirect('/')


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


def verify(request, verify_id):
    error = ''
    try:
        profile = UserProfile.objects.get(verification_id__exact=verify_id)
    except UserProfile.DoesNotExist:
        error = 'Invalid verification id'
    else:
        if 'Verified' in profile.user.groups.all():
            error = 'User already verified'
        else:
            profile.user.groups.add(Group.objects.get(name='Verified'))
            profile.user.save()
            profile.is_verified = True
            profile.save()
    return render_with_request_context(request, 'verify.html', { 'error':error, 'username':profile.user.username })
