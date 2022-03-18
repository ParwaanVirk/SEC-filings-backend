from tkinter.ttk import Combobox
from urllib import response
from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse
# from .products import products
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import filters
#company search call, 
#compare 2 companies call, 
from company.models import CompFav, Forms, Metrics, CompanyS, Performance
from company.serializers import CompanySSerializer, FormsSerializer, MetricsSerializer, PerformanceSerializer
from rest_framework import generics
class CompanyData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args,**kwargs):
        cuser = request.user
        comp_cik = request.data.get('comp_cik', None)
        detail = {}
        if CompanyS.objects.filter(CIK_Number = comp_cik).exists() == True:
            starred = False
            CompanyData = CompanyS.objects.filter(CIK_Number = comp_cik)[0]
            CompanyData.count = CompanyData.count +1
            FormData = Forms.objects.filter(CompanyS = CompanyData)
            MetricsData = Metrics.objects.filter(CompanyS = CompanyData)
            PerformanceData = Performance.objects.filter(CompanyS = CompanyData)
            SerializedCompanyData = CompanySSerializer(CompanyData)
            SerializedFormData = FormsSerializer(FormData, many = True)
            SerializedMetricsData = MetricsSerializer(MetricsData, many = True)
            SerializedPerformanceData = PerformanceSerializer(PerformanceData, many = True)
            if CompFav.objects.filter(account = cuser, CompanyS = CompanyData).exists() == True:
                starred = True
            detail['company_data']=  SerializedCompanyData.data, 
            detail['forms_data']= SerializedFormData.data, 
            detail['metrics_data']= SerializedMetricsData.data, 
            detail['performance_data']= SerializedPerformanceData.data, 
            detail['starred']= starred,
            return Response(data = detail,status = 200)
        else:
            detail['error'] = "CIK number not found"
            return Response(data = "", status = 404)



class Mostsearch(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, *args, **kwargs):
        companies = CompanyS.objects.all().order_by('-count')[0:10]
        serialized_company_data = CompanySSerializer(companies, many = True)
        return Response(data = serialized_company_data.data, status = 200)
    

class Favourites(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        cuser = request.user
        if cuser != None:
            if CompFav.objects.filter(account = cuser).exists() == True:
                favdata = CompFav.objects.filter(account = cuser)
                Compdata = []
                for element in favdata:
                    # comp = CompanyS.objects.filter(CIK_Number = )
                    Compdata.append(element.CompanyS)
                SerializedCompData = CompanySSerializer(Compdata, many = True)
                return response(data = SerializedCompData.data, status = 200)
    
    def post(self, request, *args, **kwargs):
        cuser = request.user
        if cuser != None:
            comp_cik = request.data.get('comp_cik', None)
            if CompanyS.objects.filter(CIK_Number = comp_cik).exists() == True:
                Comp = CompanyS.objects.filter(CIK_Number = comp_cik)[0]
                if CompFav.objects.filter(account = cuser, CompanyS = Comp).exists() == True:
                    return Response(data = "Success", status = 200)

                else:
                    CompFav.objects.create(
                        acocunt = cuser, 
                        CompanyS = Comp,
                    )
                    return response(data = "Success", status = 200)
    
    def delete(self, request, *args, **kwargs):
        cuser = request.user
        if cuser != None:
            comp_cik = request.data.get('comp_cik', None)
            if CompanyS.objects.filter(CIK_Number = comp_cik).exists() == True:
                Comp = CompanyS.objects.filter(CIK_Number = comp_cik)[0]
                if CompFav.objects.filter(account = cuser, CompanyS = Comp).exists() == True:
                    Cf = CompFav.objects.filter(account = cuser, CompanyS = Comp)[0].delete()
                    return response(data = "Success", status = 200)
        
            
class CompareComp(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        cuser = request.user
        if cuser != None:
            comp1_cik = request.data.get('comp1_cik',None)
            comp2_cik = request.data.get('comp2_cik', None)
            if CompanyS.objects.filter(CIK_Number = comp1_cik).exists() == True and CompanyS.objects.filter(CIK_Number = comp2_cik).exists() == True:
                CompanyData1 = CompanyS.objects.filter(CIK_Number = comp1_cik)[0]
                MetricsData1 = Metrics.objects.filter(CompanyS = CompanyData1)
                PerformanceData1 = Performance.objects.filter(CompanyS = CompanyData1)
                SerializedCompanyData1 = CompanySSerializer(CompanyData1)
                SerializedMetricsData1 = MetricsSerializer(MetricsData1, many = True)
                SerializedPerformanceData1 = PerformanceSerializer(PerformanceData1, many = True)
                
                CompanyData2 = CompanyS.objects.filter(CIK_Number = comp2_cik)[0]
                MetricsData2 = Metrics.objects.filter(CompanyS = CompanyData2)
                PerformanceData2 = Performance.objects.filter(CompanyS = CompanyData2)
                SerializedCompanyData2 = CompanySSerializer(CompanyData2)
                SerializedMetricsData2 = MetricsSerializer(MetricsData2, many = True)
                SerializedPerformanceData2 = PerformanceSerializer(PerformanceData2, many = True)

                Comp1_data = {
                    'Cdata' : SerializedCompanyData1.data, 
                    'Mdata' : SerializedMetricsData1.data, 
                    'Pdata' : SerializedPerformanceData1.data, 
                }
                Comp2_data = {
                    'Cdata' : SerializedCompanyData2.data, 
                    'Mdata' : SerializedMetricsData2.data, 
                    'Pdata' : SerializedPerformanceData2.data, 
                }

                detail = {
                    'comp1': Comp1_data,
                    'comp2': Comp2_data,
                }
                return response(data = detail, status = 200)


class CompSearch(generics.ListCreateAPIView):
    search_fields = ['Name', 'CIK_Number']
    filter_backends = (filters.SearchFilter, )
    queryset = CompanyS.objects.all()
    serializer_class = CompanySSerializer

