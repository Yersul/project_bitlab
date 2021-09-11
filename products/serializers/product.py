from rest_framework import serializers

from products.models import Product, ProductAttachment


class ProductAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = ProductAttachment
        fields = (
            'uuid',
            'file'
        )


class ProductAttachmentCreateSerializer(serializers.Serializer):
    uuid = serializers.PrimaryKeyRelatedField(queryset=ProductAttachment.objects.all())


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = (
            'uuid',
            'name',
            'description',
            'cost',
            'owner',
        )
        read_only_fields = ('created_at', 'updated_at')


class ProductCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    attachments = ProductAttachmentCreateSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = (
            'uuid',
            'name',
            'description',
            'cost',
            'owner',
            'attachments'
        )
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        attachments = validated_data.pop('attachments', None)

        instance=super().create(validated_data)

        if attachments:
            for attachment_data in attachments:
                attachment = attachment_data['uuid']
                attachment.product = instance
                attachment.save(update_fields=['product'])

        return instance


class ProductAttachmentDeleteSerializer(serializers.Serializer):
    attachments = ProductAttachmentCreateSerializer(required=True, many=True)

    class Meta:
        fields = (
            'attachments',
        )

    def delete_attachments(self):
        request = self.context['request']
        attachments = request.data['attachments']
        queryset = ProductAttachment.objects.all()
        for attachment_data in attachments:
            instance = queryset.get(pk=attachment_data['uuid'])
            instance.delete()
