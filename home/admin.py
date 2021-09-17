from django.contrib import admin

# Register your models here.
from home.models import Setting, Slideshow


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'j_date', 'status']


class SlideshowAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'status', 'ordering_position']


admin.site.register(Setting, SettingAdmin)
admin.site.register(Slideshow, SlideshowAdmin)
