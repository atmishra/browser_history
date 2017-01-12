from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
# Create your views here.

from .models import Link, UserHistory
from .serializer import LinkSerializer

import jsonpickle
from utils.stack import Stack
from itertools import chain


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
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        links = self.links

        if len(links) == 1 and links[0] == -1:
            links = Link.objects.none()

        else:
            links_list = []
            for id in links:
                if id > 0:
                    links_list.append(Link.objects.get(pk=id))
            none_qs = Link.objects.none()
            links = list(chain(none_qs, links_list))

        return links

    def updateStack(self, user, action):
        links = []

        if action:

            try:
                history = UserHistory.objects.get(user=user)

                stack = jsonpickle.decode(history.stack)

                last_ten = jsonpickle.decode(history.last_ten)

                if action == 'back':

                    link = stack.back()
                    links.append(link)
                    last_ten.append(link)

                elif action == 'forward':
                    link = stack.forward()
                    links.append(link)
                    last_ten.append(link)

                elif action == 'list':
                    links = list(last_ten)

                stack = jsonpickle.encode(stack)
                last_ten = jsonpickle.encode(last_ten)

                history.stack = stack
                history.last_ten = last_ten

            except ObjectDoesNotExist:

                links.append(-1)

            history.save()

        return links

    # def object_decoder(self, obj):

    #     if 'current_index' in obj and 'items' in obj:
    #         return Stack(obj['items'], obj['current_index'])
    #     return obj
