from django.contrib import admin
from .models import Ad, Category
# Register your models here.

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "owner", "created_at")
    list_filter = ("status", "category")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category)
