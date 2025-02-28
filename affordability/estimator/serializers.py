from rest_framework import serializers
from .models import AffordabilityInput

class AffordabilityInputSerializer(serializers.ModelSerializer):
    location = serializers.CharField(required=False, default='Seattle, WA')

    class Meta:
        model = AffordabilityInput
        fields = ['income', 'down_payment', 'loan_term', 'interest_rate', 'location']
