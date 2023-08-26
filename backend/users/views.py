from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .models import User, Subscriptions
from .serializers import (UserSerializer,
                          SetPasswordSerializer,
                          AuthorSerializer,
                          SignUpSerializer)
from .utils import PermissionPolicyMixin


class UserViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
    permission_classes_per_method = {
        "list": [AllowAny, ],
        "retrieve": [IsAuthenticated, ]
    }

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return UserSerializer
        if self.request.method == "POST":
            return SignUpSerializer

    @action(methods=['get'], detail=False, url_path='me',
            permission_classes=[IsAuthenticated, ])
    def get_profile(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["post"], detail=False,
            permission_classes=[IsAuthenticated, ])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["get"], detail=False,
            permission_classes=[IsAuthenticated, ])
    def subscriptions(self, request):
        user = request.user
        authors_id = Subscriptions.objects.filter(
            subscriber=user
        ).values('author')
        authors = User.objects.filter(id__in=authors_id)

        serializer = AuthorSerializer(authors, many=True,
                                      context={'request': request})
        queryset = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(queryset)

    @action(['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated, ])
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        user = request.user
        if user.id != author.id:
            if request.method == 'POST' and (
                not user.subscriber.filter(author=author).exists()
            ):
                Subscriptions.objects.create(author=author, subscriber=user)
                return Response(status=status.HTTP_201_CREATED)
            subscriptions = Subscriptions.objects.filter(author=author,
                                                         subscriber=user)
            if subscriptions:
                subscriptions.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
