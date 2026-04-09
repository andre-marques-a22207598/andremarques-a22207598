from django.contrib import admin

# Register your models here.
class OwnerAdmin(admin.ModelAdmin):
admin.site.register(Owner, OwnerAdmin)