from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AffordabilityInput
from .serializers import AffordabilityInputSerializer
from decimal import Decimal

class AffordabilityEstimator(APIView):
    def post(self,request):
        serializer = AffordabilityInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            monthly_income = data['income']/12
            monthly_budget = monthly_income * 0.3 # assuming 30% of monthly income can be used for mortgage payments

            loan_term_months = data['loan_term']*12
            interest_rate_monthly = data['interest_rate']/100/12

            # loan formula: PMT = [P * r(1+r)^n] / [(1+r)^n - 1]
            if interest_rate_monthly > 0:
                max_loan = monthly_budget / ((1 - (1 + interest_rate_monthly)**(-loan_term_months)) / interest_rate_monthly)
            else:
                max_loan = monthly_budget * loan_term_months

            # Total home price = loan + down payment
            max_home_price = max_loan + data['down_payment']

            max_home_price = round(Decimal(max_home_price), 2)

            return Response({'max_home_price': float(max_home_price)}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

