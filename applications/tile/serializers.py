from rest_framework import serializers

from applications.tile.models import TileImage


class TileImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TileImage
        fields = ['img', 'name']
