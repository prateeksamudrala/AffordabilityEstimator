from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AffordabilityInput
from .serializers import AffordabilityInputSerializer
from decimal import Decimal
from redfin import Redfin

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

            # Get Redfin listings
            location = request.data.get('location', 'Seattle, WA')  # Default location
            properties = self.get_redfin_listings(location, max_home_price)

            return Response({'max_home_price': float(max_home_price)}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def get_redfin_listings(self, location, max_price):
    """Fetches property listings from Redfin API"""
    client = Redfin()
    try:
        response = client.search(location)
        print("Redfin Search Response:", response)  # Debugging

        if 'payload' not in response or 'exactMatch' not in response['payload']:
            return [{"error": "No exact match for location"}]

        property_url = response['payload']['exactMatch']['url']
        print("Property URL:", property_url)  # Debugging

        listings = client.initial_info(property_url)
        print("Listings Response:", listings)  # Debugging

        if 'payload' not in listings or 'homes' not in listings['payload']:
            return [{"error": "No homes found"}]

        homes = listings['payload']['homes']
        filtered_properties = []

        for home in homes:
            price = home.get('price', 0)
            if price and price <= float(max_price):
                filtered_properties.append({
                    "address": home.get('streetLine', 'Unknown'),
                    "price": price,
                    "beds": home.get('beds', 'N/A'),
                    "baths": home.get('baths', 'N/A'),
                    "sqft": home.get('sqft', 'N/A'),
                    "url": home.get('url', '')
                })

        print("Filtered Properties:", filtered_properties)  # Debugging
        return filtered_properties

    except Exception as e:
        return [{"error": str(e)}]
