from rest_framework import serializers
from apps.dashboard.models import Contact

class contactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"