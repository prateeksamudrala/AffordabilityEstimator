from django.urls import path
from .views import AffordabilityEstimator

urlpatterns = [
    path('affordability/', AffordabilityEstimator.as_view(), name='affordability'),
]