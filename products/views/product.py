from django.http import Http404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from products.models import Product
from products.permissions import ProductAdminOrReadOnly

from products.serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    ProductAttachmentSerializer, ProductAttachmentDeleteSerializer
)


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet,
                     ):
    queryset = Product.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer

    def get_permissions(self):
        permission_classes = [AllowAny, ]

        if self.action == 'retrieve' or self.action == 'create':
            permission_classes = [IsAuthenticated, ProductAdminOrReadOnly]
        if self.action == 'update' or self.action == 'destroy' or self.action == 'partial_update':
            permission_classes.append(ProductAdminOrReadOnly)

        return (permission() for permission in permission_classes)

    def get_serializer_class(self):
        serializer_class = ProductSerializer

        if self.action == 'create':
            serializer_class = ProductCreateSerializer
        elif self.action == 'update_attachments':
            serializer_class = ProductAttachmentSerializer
        elif self.action == 'delete_attachments':
            serializer_class = ProductAttachmentDeleteSerializer

        return serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer_data = ProductSerializer(instance).data
        return Response(data=serializer_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        # instance = self.get_products()
        serializer = self.get_serializer(self.queryset.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update_attachments(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_products(self):
        owner = self.request.user

        try:
            instance = Product.objects.filter(owner= owner)
            return instance
        except:
            raise Http404

    def get_object(self):
        uuid = self.kwargs['pk']
        try:
            instance = self.queryset.get(uuid=uuid)
            return instance
        except:
            raise Http404

    def delete_attachments(self, request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.delete_attachments()
        return Response(data = {'detail':{'all deleted'}}, status=status.HTTP_204_NO_CONTENT)
