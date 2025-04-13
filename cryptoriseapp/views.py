from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse as json
from django.db.models import F, Q
from django.views.decorators.http import require_GET as re_ge
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required as l_g
from . import models
from PIL import Image
from django.contrib import messages

# Create your views here.
@re_ge
def home(request):
    return render(request, 'home.html', )