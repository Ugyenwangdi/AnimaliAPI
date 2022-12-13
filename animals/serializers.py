from rest_framework import serializers

from .models import Animal

## Using APIView
## With view 1 OR 
## option 1..
# class AnimalSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=150)
#     kingdom = serializers.CharField(max_length=60)
#     phylum = serializers.CharField(max_length=60)
#     classname = serializers.CharField(max_length=60)
#     order = serializers.CharField(max_length=60)
#     family = serializers.CharField(max_length=60)
#     genus = serializers.CharField(max_length=60)
#     scientificname = serializers.CharField(max_length=150)
#     # contributor_id = serializers.IntegerField()
    
#     def create(self, validated_data):
#         return Animal.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.kingdom = validated_data.get('kingdom', instance.kingdom)
#         instance.phylum = validated_data.get('phylum', instance.phylum)
#         instance.classname = validated_data.get('classname', instance.classname)
#         instance.order = validated_data.get('order', instance.order)
#         instance.family = validated_data.get('family', instance.family)
#         instance.genus = validated_data.get('genus', instance.genus)
#         instance.scientificname = validated_data.get('scientificname', instance.scientificname)
#         # instance.contributor_id = validated_data.get('contributor_id', instance.contributor_id)

#         instance.save()
#         return instance


### option 2...Also this can be done with view 1 but this time it is using model serializer...keeping code more concise
class AnimalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Animal
        fields = ('id', 'name', 'kingdom', 'phylum', 'classname', 'order', 'family', 'genus', 'scientificname')