from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
# Create your views here.

from .models import Link, UserHistory
from .serializer import LinkSerializer

import json
from utils.stack import Stack


class LinkView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    links = []

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        user = self.request.user

        action = self.request.query_params.get('action', None)

        links = self.updateStack(user, action)

        self.links = links

        # if len(links) == 1 and links[0] == -1:
        #     links = Link.objects.none()

        # else:

        #     links = Link.objects.filter(pk__in=links)

        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        links = self.links

        if len(links) == 1 and links[0] == -1:
            links = Link.objects.none()

        else:

            links = Link.objects.filter(pk__in=links)

        return links

    def updateStack(self, user, action):
        links = []

        if action:

            try:
                history = UserHistory.objects.get(user=user)

                stack = json.loads(
                    history.stack, object_hook=self.object_decoder)
                if action == 'back':

                    link = stack.back()
                    links.append(link)

                elif action == 'forward':
                    link = stack.forward()
                    links.append(link)

                elif action == 'list':
                    links = stack.last_ten()

                stack = json.dumps(stack, default=lambda o: o.__dict__)
                history.stack = stack

            except ObjectDoesNotExist:

                links.append(-1)

            history.save()

        return links

    def object_decoder(self, obj):

        if 'current_index' in obj and 'items' in obj:
            return Stack(obj['items'], obj['current_index'])
        return obj
