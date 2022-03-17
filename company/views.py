from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
# from .products import products
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CompanyS
from .models import Forms
from .models import Metrics
from .models import Performance

from .serializer import CompanySSerializer
from .serializer import FormsSerializer
from .serializer import MetricsSerializer
from .serializer import PerformanceSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = ['', '/company', '/forms', '/metrics', '/performance']

    return Response(routes)


@api_view(['GET'])
def getCompanyS(request):

    comp = CompanyS.objects.all()

    serializer = CompanySSerializer(comp, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getForms(request):

    forms = Forms.objects.all()

    serializer = FormsSerializer(forms, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getMetrics(request):

    met = Metrics.objects.all()

    serializer = MetricsSerializer(met, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getPerformance(request):

    perf = Performance.objects.all()

    serializer = PerformanceSerializer(perf, many=True)

    return Response(serializer.data)
