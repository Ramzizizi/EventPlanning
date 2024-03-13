from rest_framework import serializers

from places import models as place_models


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = place_models.Place
        fields = ['url', 'id', 'account_name', 'users', 'created']
