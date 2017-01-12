from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Link, UserHistory
from utils.stack import Stack
import jsonpickle
import collections


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

    def checkStack(self, user, link_id):
        try:
            '''Retrieve history object if exists'''
            history = UserHistory.objects.get(user=user)

            '''Retrieve stack for the user and update it'''
            stack = jsonpickle.decode(history.stack)
            stack.push(link_id)
            stack = jsonpickle.encode(stack)

            '''Retrieve last activity for the user and update it'''
            last_ten = jsonpickle.decode(history.last_ten)
            last_ten.append(link_id)
            last_ten = jsonpickle.encode(last_ten)

            history.stack = stack
            history.last_ten = last_ten

        except ObjectDoesNotExist:

            stack = Stack()
            stack.push(link_id)
            stack = jsonpickle.encode(stack)

            last_ten = collections.deque(maxlen=10)
            last_ten.append(link_id)
            last_ten = jsonpickle.encode(last_ten)
            history = UserHistory(user=user, stack=stack, last_ten=last_ten)

        history.save()
