import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def base(request):
    context = {
        'now' : datetime.date.today()
    }
    area_url = request.META.get('PATH_INFO')
    if request.user.is_authenticated and not "/admin/" in area_url:
        objuser = request.user
        context = {
            'now': datetime.date.today(),
            "objuser" : objuser,
        }
    
    return context

@login_required
@csrf_exempt
def change_theme(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        request.user.theme = theme
        request.user.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)
