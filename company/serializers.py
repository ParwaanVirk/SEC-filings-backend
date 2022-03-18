from rest_framework import serializers
# from django.contrib.auth.models import User
from company.models import CompanyS, Forms, Metrics, Performance, CompFav


class CompanySSerializer (serializers.ModelSerializer):
    class Meta:
        model = CompanyS
        fields = '__all__'


class FormsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = '__all__'


class MetricsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Metrics
        fields = '__all__'


class PerformanceSerializer (serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'


class CompFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompFav
        fields = '__all__'