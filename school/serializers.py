from rest_framework import serializers

from school.models import Grade


class GradeSerializer(serializers.Serializer):
    test = serializers.CharField()
    student = serializers.CharField()
    value = serializers.IntegerField()

    def create(self, validated_data):
        return Grade.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance

'''

class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ['id','test','student','value']
        '''