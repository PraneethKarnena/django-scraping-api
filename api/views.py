from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def home_view(request):
    return render(request, 'api/home.html')