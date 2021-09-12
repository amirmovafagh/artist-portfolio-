from django.contrib import admin, messages
import admin_thumbnails

# Register your models here.
from django.contrib.auth.models import User
from django.utils.translation import ngettext
from mptt.admin import DraggableMPTTAdmin

from works.models import Category, Work, Gallery


def make_enable(modeladmin, request, queryset):
    updated = queryset.update(status='True')
    modeladmin.message_user(request, ngettext(
        '%d فیلد موردنظر فعال شد.',
        '%d فیلدهای موردنظر فعال شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_enable.short_description = "فعال سازی فیلد انتخاب شده"


def make_disable(modeladmin, request, queryset):
    updated = queryset.update(status='False')
    modeladmin.message_user(request, ngettext(
        '%d فیلد موردنظر غیرفعال شد.',
        '%d فیلد موردنظر غیرفعال شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_disable.short_description = "غیرفعال کردن فیلد انتخاب شده"


def make_cat_enable(modeladmin, request, queryset):
    updated = queryset.update(status=True)
    modeladmin.message_user(request, ngettext(
        '%d فیلد موردنظر فعال شد.',
        '%d فیلدهای موردنظر فعال شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_cat_enable.short_description = "فعال سازی فیلد انتخاب شده"


def make_cat_disable(modeladmin, request, queryset):
    updated = queryset.update(status=False)
    modeladmin.message_user(request, ngettext(
        '%d فیلد موردنظر غیرفعال شد.',
        '%d فیلد موردنظر غیرفعال شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_cat_disable.short_description = "غیرفعال کردن فیلد انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status', 'parent']
    actions = [make_cat_enable, make_cat_disable]


class CategoryAdminMp(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_works_count', 'related_works_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_cat_enable, make_cat_disable]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative work count
        qs = Category.objects.add_related_count(
            qs,
            Work,
            'category',
            'works_cumulative_count',
            cumulative=True)

        # Add non cumulative work count
        qs = Category.objects.add_related_count(qs,
                                                Work,
                                                'category',
                                                'works_count',
                                                cumulative=False)
        return qs

    def related_works_count(self, instance):
        return instance.works_count

    related_works_count.short_description = 'Related works (for this specific category)'

    def related_works_cumulative_count(self, instance):
        return instance.works_cumulative_count

    related_works_cumulative_count.short_description = 'Related works (in tree)'


@admin_thumbnails.thumbnail('image')
class WorkGalleryInLine(admin.TabularInline):
    model = Gallery
    readonly_fields = ('id',)
    extra = 1


class WorkAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "creator":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ['title', 'category_to_str', 'status', 'image_tag']
    list_filter = ['status', 'category']
    search_fields = ('title',)
    readonly_fields = ('image_tag',)
    inlines = [WorkGalleryInLine]
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_enable, make_disable]


@admin_thumbnails.thumbnail('image')
class WorkGallery(admin.ModelAdmin):
    list_display = ['title', 'work', 'image_tag', 'image_thumbnail']
    list_filter = ['work']
    readonly_fields = ('image_tag',)

    def has_module_permission(self, request):
        return False


admin.site.register(Category, CategoryAdminMp)
admin.site.register(Work, WorkAdmin)
admin.site.register(Gallery, WorkGallery)
