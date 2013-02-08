from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.shortcuts import *

def login_wrapper(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(reverse('auth.views.home'))
    else:
        return login(request, **kwargs)


def profile(request):
    return render_to_response('registration/profile.html',
        {},
        context_instance=RequestContext(request))


def home(request):
    return render_to_response('home.html',{},RequestContext(request))