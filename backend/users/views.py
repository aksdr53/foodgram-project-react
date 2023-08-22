from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import User, Subscriptions
from .serializers import (UserSerializer,
                          SetPasswordSerializer,
                          AuthorSerializer,
                          SignUpSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ["get", "post"]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def get_serializer_class(self, request):
        if self.action == "list" or self.action == "retrieve":
            return UserSerializer
        if self.action == "create":
            return SignUpSerializer

    @action(methods=['get'], detail=False, url_path='me',
            permission_classes=[IsAuthenticated, ])
    def get_profile(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["post"], detail=False,
            permission_classes=[IsAuthenticated, ])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

    @action(["get"],
            permission_classes=[IsAuthenticated, ])
    def subscriptions(self, request):
        authors = request.user.subscriber.all().author.all()
        serializer = AuthorSerializer(authors, many=True)
        queryset = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(queryset)

    @action(['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated, ])
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        user = request.user
        if user.id != pk and (
            not user.subscriber.filter(author=author).exists()
        ):
            if request.method == 'POST':
                Subscriptions.objects.create(author=author, user=user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            Subscriptions.objects.delete(author=author, user=user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
