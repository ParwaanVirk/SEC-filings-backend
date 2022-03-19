from urllib import response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from company.seed import seeder_10k
from company.models import CompFav, Forms, Metrics, CompanyS, Performance
from company.serializers import CompanySSerializer, FormsSerializer, MetricsSerializer, PerformanceSerializer
from rest_framework import generics

class CompanyData(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args,**kwargs):
        cuser = request.user
        comp_cik = request.GET.get('comp_cik', None)
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
            return Response(data = detail, status = 404)



class Mostsearch(APIView):
    def get(self,request, *args, **kwargs):
        companies = CompanyS.objects.all().order_by('-count')[0:10]
        serialized_company_data = CompanySSerializer(companies, many = True)
        response_dict = {}
        response_dict['data'] = serialized_company_data.data

        return Response(data = response_dict, status = 200)


class Favourites(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        cuser = request.user
        response_dict = {}

        if CompFav.objects.filter(account = cuser).exists() == True:
            favdata = CompFav.objects.filter(account = cuser)
            Compdata = []

            for element in favdata:
                Compdata.append(element.CompanyS)
            SerializedCompData = CompanySSerializer(Compdata, many = True)
            response_dict['data'] = SerializedCompData.data

        else:
            response_dict['data'] = []

        return Response(data = response_dict, status = 200)

    def post(self, request, *args, **kwargs):
        cuser = request.user
        response_dict = {}
        comp_cik = request.data.get('comp_cik', None)

        if CompanyS.objects.filter(CIK_Number = comp_cik).exists() == True:
            Comp = CompanyS.objects.filter(CIK_Number = comp_cik)[0]

            if CompFav.objects.filter(account = cuser, CompanyS = Comp).exists() == True:
                response_dict['data'] = None
                response_dict['success'] = True
                return Response(data = response_dict, status = 200)

            else:
                CompFav.objects.create(
                    account = cuser,
                    CompanyS = Comp,
                )
                response_dict['data'] = None
                response_dict['success'] = True
                return Response(data = response_dict, status = 200)

    def delete(self, request, *args, **kwargs):

        cuser = request.user
        response_dict = {}
        comp_cik = request.GET.get('comp_cik', None)

        if CompanyS.objects.filter(CIK_Number = comp_cik).exists() == True:
            Comp = CompanyS.objects.filter(CIK_Number = comp_cik)[0]

            if CompFav.objects.filter(account = cuser, CompanyS = Comp).exists() == True:
                Cf = CompFav.objects.filter(account = cuser, CompanyS = Comp)[0].delete()
                response_dict['data'] = None
                response_dict['success'] = True
                return Response(data = response_dict, status = 200)


class CompSearch(generics.ListCreateAPIView):
    search_fields = ['Name', 'CIK_Number']
    filter_backends = (filters.SearchFilter, )
    queryset = CompanyS.objects.all()
    serializer_class = CompanySSerializer

class Seeding(APIView):
    def get(self, request, *args, **kwargs):
        seeder_10k()
        return Response(data = "Success", status = 200)
