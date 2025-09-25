# # apps/products/serializers.py

# """
# Product Serializers

# Clean serializers with proper validations for the 3 essential APIs.
# """

# from rest_framework import serializers
# from decimal import Decimal
# from .models import Product, Category


# class ProductListSerializer(serializers.ModelSerializer):
#     """Serializer for Product list view (minimal data)"""
    
#     category_name = serializers.CharField(source='category.name', read_only=True)
#     primary_image = serializers.SerializerMethodField(read_only=True)
#     stock_status = serializers.CharField(read_only=True)
#     discount_percentage = serializers.FloatField(read_only=True)
#     is_on_sale = serializers.BooleanField(read_only=True)
    
#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'name',
#             'slug',
#             'short_description',
#             'price',
#             'compare_price',
#             'category_name',
#             'primary_image',
#             'stock_status',
#             'stock_quantity',
#             'discount_percentage',
#             'is_on_sale',
#             'is_featured',
#             'created_at'
#         ]
    
#     def get_primary_image(self, obj):
#         """Get primary image URL"""
#         primary_image = obj.images.filter(is_primary=True).first()
#         if primary_image:
#             request = self.context.get('request')
#             if request:
#                 return request.build_absolute_uri(primary_image.image.url)
#             return primary_image.image.url
#         return None


# class ProductDetailSerializer(serializers.ModelSerializer):
#     """Serializer for Product detail view (complete data)"""
    
#     category_name = serializers.CharField(source='category.name', read_only=True)
#     stock_status = serializers.CharField(read_only=True)
#     discount_percentage = serializers.FloatField(read_only=True)
#     is_on_sale = serializers.BooleanField(read_only=True)
    
#     class Meta:
#         model = Product
#         fields = [
#             'id',
#             'name',
#             'slug',
#             'description',
#             'short_description',
#             'price',
#             'compare_price',
#             'sku',
#             'stock_quantity',
#             'low_stock_threshold',
#             'stock_status',
#             'category_name',
#             'is_active',
#             'is_featured',
#             'discount_percentage',
#             'is_on_sale',
#             'meta_title',
#             'meta_description',
#             'created_at',
#             'updated_at'
#         ]


# class ProductCreateSerializer(serializers.ModelSerializer):
#     """Serializer for creating products with comprehensive validations"""
    
#     category_id = serializers.UUIDField(required=True)
    
#     class Meta:
#         model = Product
#         fields = [
#             'name',
#             'description',
#             'short_description',
#             'price',
#             'compare_price',
#             'stock_quantity',
#             'low_stock_threshold',
#             'category_id',
#             'is_active',
#             'is_featured',
#             'meta_title',
#             'meta_description'
#         ]
    
#     def validate_name(self, value):
#         """Validate product name"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Product name is required.")
        
#         if len(value.strip()) < 3:
#             raise serializers.ValidationError("Product name must be at least 3 characters long.")
        
#         if len(value) > 200:
#             raise serializers.ValidationError("Product name cannot exceed 200 characters.")
        
#         # Check for existing product with same name
#         if Product.objects.filter(name__iexact=value.strip()).exists():
#             raise serializers.ValidationError("A product with this name already exists.")
        
#         return value.strip()
    
#     def validate_description(self, value):
#         """Validate product description"""
#         if not value or not value.strip():
#             raise serializers.ValidationError("Product description is required.")
        
#         if len(value.strip()) < 10:
#             raise serializers.ValidationError("Product description must be at least 10 characters long.")
        
#         return value.strip()
    
#     def validate_short_description(self, value):
#         """Validate short description"""
#         if value and len(value) > 300:
#             raise serializers.ValidationError("Short description cannot exceed 300 characters.")
        
#         return value.strip() if value else ""
    
#     def validate_price(self, value):
#         """Validate product price"""
#         if value is None:
#             raise serializers.ValidationError("Price is required.")
        
#         if value <= 0:
#             raise serializers.ValidationError("Price must be greater than zero.")
        
#         if value > Decimal('999999.99'):
#             raise serializers.ValidationError("Price cannot exceed 999,999.99.")
        
#         # Check decimal places
#         if value.as_tuple().exponent < -2:
#             raise serializers.ValidationError("Price can have maximum 2 decimal places.")
        
#         return value
    
#     def validate_compare_price(self, value):
#         """Validate compare price"""
#         if value is not None:
#             if value <= 0:
#                 raise serializers.ValidationError("Compare price must be greater than zero.")
            
#             if value > Decimal('999999.99'):
#                 raise serializers.ValidationError("Compare price cannot exceed 999,999.99.")
            
#             # Check decimal places
#             if value.as_tuple().exponent < -2:
#                 raise serializers.ValidationError("Compare price can have maximum 2 decimal places.")
        
#         return value
    
#     def validate_stock_quantity(self, value):
#         """Validate stock quantity"""
#         if value is None:
#             raise serializers.ValidationError("Stock quantity is required.")
        
#         if value < 0:
#             raise serializers.ValidationError("Stock quantity cannot be negative.")
        
#         if value > 999999:
#             raise serializers.ValidationError("Stock quantity cannot exceed 999,999.")
        
#         return value
    
#     def validate_low_stock_threshold(self, value):
#         """Validate low stock threshold"""
#         if value is not None and value < 0:
#             raise serializers.ValidationError("Low stock threshold cannot be negative.")
        
#         return value or 10  # Default to 10 if not provided
    
#     def validate_category_id(self, value):
#         """Validate category exists and is active"""
#         if not value:
#             raise serializers.ValidationError("Category is required.")
        
#         try:
#             category = Category.objects.get(id=value, is_active=True)
#             return value
#         except Category.DoesNotExist:
#             raise serializers.ValidationError("Invalid category or category is not active.")
    
#     def validate_meta_title(self, value):
#         """Validate meta title"""
#         if value and len(value) > 60:
#             raise serializers.ValidationError("Meta title cannot exceed 60 characters.")
        
#         return value.strip() if value else ""
    
#     def validate_meta_description(self, value):
#         """Validate meta description"""
#         if value and len(value) > 160:
#             raise serializers.ValidationError("Meta description cannot exceed 160 characters.")
        
#         return value.strip() if value else ""
    
#     def validate(self, attrs):
#         """Cross-field validation"""
#         price = attrs.get('price')
#         compare_price = attrs.get('compare_price')
#         stock_quantity = attrs.get('stock_quantity')
#         low_stock_threshold = attrs.get('low_stock_threshold')
        
#         # Validate compare_price vs price
#         if compare_price and price and compare_price <= price:
#             raise serializers.ValidationError({
#                 'compare_price': 'Compare price must be greater than the selling price.'
#             })
        
#         # Validate low_stock_threshold vs stock_quantity
#         if low_stock_threshold and stock_quantity and low_stock_threshold > stock_quantity:
#             raise serializers.ValidationError({
#                 'low_stock_threshold': 'Low stock threshold cannot be greater than current stock quantity.'
#             })
        
#         return attrs
    
#     def create(self, validated_data):
#         """Create product with category"""
#         category_id = validated_data.pop('category_id')
#         category = Category.objects.get(id=category_id)
        
#         product = Product.objects.create(
#             category=category,
#             **validated_data
#         )
#         return product



# apps/products/serializers.py

"""
Product Serializers

Complete serializers with proper validations for all CRUD operations.
"""

from rest_framework import serializers
from decimal import Decimal
from .models import Product, Category, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for Product Images"""
    
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'alt_text', 'is_primary', 'order']
    
    def get_image_url(self, obj):
        """Get full image URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for Product list view (minimal data for performance)"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    primary_image = serializers.SerializerMethodField(read_only=True)
    stock_status = serializers.CharField(read_only=True)
    discount_percentage = serializers.FloatField(read_only=True)
    is_on_sale = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'short_description',
            'price',
            'compare_price',
            'sku',
            'stock_quantity',
            'category_name',
            'category_slug',
            'primary_image',
            'stock_status',
            'discount_percentage',
            'is_on_sale',
            'is_featured',
            'is_active',
            'created_at'
        ]
    
    def get_primary_image(self, obj):
        """Get primary image URL"""
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for Product detail view (complete data)"""
    
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    stock_status = serializers.CharField(read_only=True)
    discount_percentage = serializers.FloatField(read_only=True)
    is_on_sale = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'short_description',
            'price',
            'compare_price',
            'sku',
            'stock_quantity',
            'low_stock_threshold',
            'stock_status',
            'category',
            'images',
            'is_active',
            'is_featured',
            'discount_percentage',
            'is_on_sale',
            'meta_title',
            'meta_description',
            'created_at',
            'updated_at'
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating products with comprehensive validations"""
    
    category_id = serializers.UUIDField(required=True, write_only=True)
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'short_description',
            'price',
            'compare_price',
            'stock_quantity',
            'low_stock_threshold',
            'category_id',
            'is_active',
            'is_featured',
            'meta_title',
            'meta_description'
        ]
    
    def validate_name(self, value):
        """Validate product name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Product name is required.")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters long.")
        
        if len(value) > 200:
            raise serializers.ValidationError("Product name cannot exceed 200 characters.")
        
        # Check for existing product with same name (exclude self for updates)
        queryset = Product.objects.filter(name__iexact=value.strip())
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        
        if queryset.exists():
            raise serializers.ValidationError("A product with this name already exists.")
        
        return value.strip()
    
    def validate_description(self, value):
        """Validate product description"""
        if not value or not value.strip():
            raise serializers.ValidationError("Product description is required.")
        
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Product description must be at least 10 characters long.")
        
        return value.strip()
    
    def validate_short_description(self, value):
        """Validate short description"""
        if value and len(value) > 300:
            raise serializers.ValidationError("Short description cannot exceed 300 characters.")
        
        return value.strip() if value else ""
    
    def validate_price(self, value):
        """Validate product price"""
        if value is None:
            raise serializers.ValidationError("Price is required.")
        
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        
        if value > Decimal('999999.99'):
            raise serializers.ValidationError("Price cannot exceed 999,999.99.")
        
        # Check decimal places
        if value.as_tuple().exponent < -2:
            raise serializers.ValidationError("Price can have maximum 2 decimal places.")
        
        return value
    
    def validate_compare_price(self, value):
        """Validate compare price"""
        if value is not None:
            if value <= 0:
                raise serializers.ValidationError("Compare price must be greater than zero.")
            
            if value > Decimal('999999.99'):
                raise serializers.ValidationError("Compare price cannot exceed 999,999.99.")
            
            # Check decimal places
            if value.as_tuple().exponent < -2:
                raise serializers.ValidationError("Compare price can have maximum 2 decimal places.")
        
        return value
    
    def validate_stock_quantity(self, value):
        """Validate stock quantity"""
        if value is None:
            raise serializers.ValidationError("Stock quantity is required.")
        
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        
        if value > 999999:
            raise serializers.ValidationError("Stock quantity cannot exceed 999,999.")
        
        return value
    
    def validate_low_stock_threshold(self, value):
        """Validate low stock threshold"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Low stock threshold cannot be negative.")
        
        return value or 10  # Default to 10 if not provided
    
    def validate_category_id(self, value):
        """Validate category exists and is active"""
        if not value:
            raise serializers.ValidationError("Category is required.")
        
        try:
            category = Category.objects.get(id=value, is_active=True)
            return value
        except Category.DoesNotExist:
            raise serializers.ValidationError("Invalid category or category is not active.")
    
    def validate_meta_title(self, value):
        """Validate meta title"""
        if value and len(value) > 60:
            raise serializers.ValidationError("Meta title cannot exceed 60 characters.")
        
        return value.strip() if value else ""
    
    def validate_meta_description(self, value):
        """Validate meta description"""
        if value and len(value) > 160:
            raise serializers.ValidationError("Meta description cannot exceed 160 characters.")
        
        return value.strip() if value else ""
    
    def validate(self, attrs):
        """Cross-field validation"""
        price = attrs.get('price')
        compare_price = attrs.get('compare_price')
        stock_quantity = attrs.get('stock_quantity')
        low_stock_threshold = attrs.get('low_stock_threshold')
        
        # Validate compare_price vs price
        if compare_price and price and compare_price <= price:
            raise serializers.ValidationError({
                'compare_price': 'Compare price must be greater than the selling price.'
            })
        
        # Validate low_stock_threshold vs stock_quantity
        if low_stock_threshold and stock_quantity and low_stock_threshold > stock_quantity:
            raise serializers.ValidationError({
                'low_stock_threshold': 'Low stock threshold cannot be greater than current stock quantity.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create product with category"""
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        
        product = Product.objects.create(
            category=category,
            **validated_data
        )
        return product
    
    def update(self, instance, validated_data):
        """Update product with category"""
        category_id = validated_data.pop('category_id', None)
        
        if category_id:
            category = Category.objects.get(id=category_id)
            instance.category = category
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance



class CategoryListSerializer(serializers.ModelSerializer):
    """Serializer for Category list view"""
    
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'image',
            'products_count',
            'is_active',
            'created_at'
        ]
    
    def get_products_count(self, obj):
        """Get count of active products in this category"""
        return obj.products.filter(is_active=True).count()


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Serializer for Category detail view"""
    
    products_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'image',
            'image_url',
            'products_count',
            'is_active',
            'created_at',
            'updated_at'
        ]
    
    def get_products_count(self, obj):
        """Get count of active products in this category"""
        return obj.products.filter(is_active=True).count()
    
    def get_image_url(self, obj):
        """Get full image URL"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating categories"""
    
    class Meta:
        model = Category
        fields = [
            'name',
            'description',
            'image',
            'is_active'
        ]
    
    def validate_name(self, value):
        """Validate category name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Category name is required.")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Category name must be at least 2 characters long.")
        
        if len(value) > 100:
            raise serializers.ValidationError("Category name cannot exceed 100 characters.")
        
        # Check for existing category with same name (exclude self for updates)
        queryset = Category.objects.filter(name__iexact=value.strip())
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        
        if queryset.exists():
            raise serializers.ValidationError("A category with this name already exists.")
        
        return value.strip()
    
    def validate_description(self, value):
        """Validate category description"""
        if value and len(value) > 500:
            raise serializers.ValidationError("Description cannot exceed 500 characters.")
        
        return value.strip() if value else ""    