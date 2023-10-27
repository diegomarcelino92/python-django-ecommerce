from django.contrib import admin

from products.models import Product, Variation


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    model = Variation
    list_display = ('name', 'price', 'price_promo', 'stock')
    search_fields = ('name',)
    verbose_name_plural = 'variations'


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name', 'price', 'price_promo', 'type')
    list_filter = ('type',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [VariationInline]
