from django.shortcuts import render
from django.views.decorators.http import require_GET
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import AllowAny


@require_GET
def home_view(request):
    return render(request, 'api/home.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def scrape_view(request):
    pass