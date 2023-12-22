from django.shortcuts import render, redirect, reverse

# Create your account task here.


def Franchise_Session_Required(function):
    def wrap(request, *args, **kwargs):
        if(request.session.has_key('LoggedInFranchise')):
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('franchises:login'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def Franchise_Session_Not_Required(function):
    def wrap(request, *args, **kwargs):
        if not request.session.has_key('LoggedInFranchise'):
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('franchises:dashboard'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
