from rest_framework import serializers
from .models import Super
from .models import Power

class PowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Power
        fields = ['id', 'name']

class SuperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Super
        fields = ['id', 'name', 'alter_ego', 'powers', 'catchphrase', 'super_type']
        # fields = ['id', 'name', 'alter_ego', 'primary_ability', 'secondary_ability', 'catchphrase', 'super_type']
        # depth = 1