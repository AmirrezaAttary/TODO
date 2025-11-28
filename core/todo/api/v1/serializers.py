from rest_framework import serializers
from todo.models import Task
from accounts.models import User

class TaskSerializer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source='get_absolute_api_url',read_only=True)
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ["id",'user','title','complete','relative_url','absolute_url','created_date']
        read_only_fields = ["id",'user']

    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context['kwargs'].get('pk'):
            rep.pop('relative_url',None)
            rep.pop('absolute_url',None)
        return rep


    def create(self, validated_data):
        validated_data['user'] = User.objects.get(id=self.context['request'].user.id)
        return super().create(validated_data)