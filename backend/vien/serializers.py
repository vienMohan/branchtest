from rest_framework import serializers
from .models import *

class EmpSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])  # ✅ Add this

    class Meta:
        model = Candidate
        fields = '__all__'  # This will include all fields from the Emp model

    
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = '__all__'

class OpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Openings
        fields = '__all__'