from rest_framework import serializers

from .models import Products, Size, Color, SubVariant


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'size']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'color']


class SubVariantSerializer(serializers.ModelSerializer):
    size = serializers.CharField()
    color = serializers.CharField()

    class Meta:
        model = SubVariant
        fields = ['id', 'size', 'color', 'stock']

    def to_internal_value(self, data):
        # Convert size and color to lowercase
        size = data.get('size', '').lower()
        color = data.get('color', '').lower()
        data['size'] = size
        data['color'] = color
        return super().to_internal_value(data)

    def validate(self, data):
        size = data.get('size')
        color = data.get('color')

        try:
            size_instance = Size.objects.get(size=size)
        except Size.DoesNotExist:
            raise serializers.ValidationError({'size': 'Size not found'})

        try:
            color_instance = Color.objects.get(color=color)
        except Color.DoesNotExist:
            raise serializers.ValidationError({'color': 'Color not found'})

        data['size'] = size_instance
        data['color'] = color_instance
        return data


class AddStockSerializer(serializers.ModelSerializer):
    size = serializers.CharField()
    color = serializers.CharField()

    class Meta:
        model = SubVariant
        fields = ['product', 'size', 'color', 'stock']

    def validate(self, data):
        size = data['size']
        color = data['color']

        try:
            size_instance = Size.objects.get(size=size)
        except Size.DoesNotExist:
            raise serializers.ValidationError({'size': 'Size not found'})

        try:
            color_instance = Color.objects.get(color=color)
        except Color.DoesNotExist:
            raise serializers.ValidationError({'color': 'Color not found'})

        data['size'] = size_instance
        data['color'] = color_instance

        if not SubVariant.objects.filter(
                product=data['product'],
                size=size_instance,
                color=color_instance
        ).exists():
            raise serializers.ValidationError("The specified subvariant does not exist.")
        return data


class RemoveStockSerializer(serializers.ModelSerializer):
    size = serializers.CharField()
    color = serializers.CharField()

    class Meta:
        model = SubVariant
        fields = ['product', 'size', 'color', 'stock']

    def validate(self, data):
        size = data['size']
        color = data['color']

        try:
            size_instance = Size.objects.get(size=size)
        except Size.DoesNotExist:
            raise serializers.ValidationError({'size': 'Size not found'})

        try:
            color_instance = Color.objects.get(color=color)
        except Color.DoesNotExist:
            raise serializers.ValidationError({'color': 'Color not found'})

        data['size'] = size_instance
        data['color'] = color_instance

        if not SubVariant.objects.filter(
                product=data['product'],
                size=size_instance,
                color=color_instance
        ).exists():
            raise serializers.ValidationError("The specified subvariant does not exist.")

        subvariant = SubVariant.objects.get(
            product=data['product'],
            size=size_instance,
            color=color_instance
        )
        if data['stock'] > subvariant.stock:
            raise serializers.ValidationError("Insufficient stock to remove.")

        return data


class ProductsSerializer(serializers.ModelSerializer):
    subvariants = SubVariantSerializer(many=True, required=False)

    class Meta:
        model = Products
        fields = ['id', 'ProductID', 'ProductCode', 'ProductName', 'ProductImage', 'CreatedUser', 'IsFavourite',
                  'Active', 'HSNCode', 'subvariants']

    def create(self, validated_data):
        subvariants_data = validated_data.pop('subvariants', [])
        product = Products.objects.create(**validated_data)

        for subvariant_data in subvariants_data:
            size = subvariant_data.pop('size')
            color = subvariant_data.pop('color')

            size_instance = Size.objects.get(size=size)
            color_instance = Color.objects.get(color=color)

            SubVariant.objects.create(
                product=product,
                size=size_instance,
                color=color_instance,
                stock=subvariant_data['stock']
            )
        return product
