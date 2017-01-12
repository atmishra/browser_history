from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Link, UserHistory
from utils.stack import Stack
import json


class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = ('id', 'url', 'created_on')
        read_only_fields = ('created_on',)

    '''Check if link url already exist in the database'''

    def create(self, validated_data):
        link, created = Link.objects.get_or_create(url=validated_data['url'])
        user = self.context['request'].user
        self.checkStack(user, link.id)
        return link

    def object_decoder(self, obj):

        if 'current_index' in obj and 'items' in obj:
            return Stack(obj['items'], obj['current_index'])
        return obj

    def checkStack(self, user, link_id):
        try:
            history = UserHistory.objects.get(user=user)

            stack = json.loads(history.stack, object_hook=self.object_decoder)
            stack.push(link_id)
            stack = json.dumps(stack, default=lambda o: o.__dict__)
            history.stack = stack

        except ObjectDoesNotExist:

            stack = Stack()
            stack.push(link_id)
            stack = json.dumps(stack, default=lambda o: o.__dict__)
            history = UserHistory(user=user, stack=stack)

        history.save()
