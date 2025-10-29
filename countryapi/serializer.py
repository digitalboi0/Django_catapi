from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "capital", "region",
                 "population", "currency_code", "estimated_gdp", "exchange_rate", "flag_url",
                 "last_refreshed_at"
        ]
        
        read_only_fields = ["id", "last_refreshed_at"]