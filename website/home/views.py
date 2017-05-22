from django.shortcuts import render
from django.http import HttpResponse

from .models import TopHashTags, TopUserMentions

import os
import time
import unittest


def index(request):

    context = {'topics': ['4', '5', '7', '8', '17']}
    return render(request, 'home/index.html', context)


