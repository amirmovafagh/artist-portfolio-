from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from extensions.utils import jalali_converter


class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL,
                            verbose_name='والد')
    title = models.CharField(max_length=50, unique=True, verbose_name='دسته بندی')
    keywords = models.CharField(max_length=255, blank=True, verbose_name='کلمات کلیدی')
    description = models.CharField(max_length=255, blank=True, verbose_name='توضیحات')
    image = models.ImageField(blank=True, upload_to='images/', verbose_name='تصویر')
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    slug = models.SlugField(max_length=100, unique=True, null=False, verbose_name="آدرس دسته بندی")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('works:WorkDetail', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'

    class Meta:
        verbose_name = 'دسته\u200cبندی'
        verbose_name_plural = 'دسته\u200cبندی\u200cها'


class WorkManager(models.Manager):
    def active(self):
        return self.filter(status='True')


class Work(models.Model):
    STATUS = (
        ('True', 'فعال'),
        ('False', 'غیرغعال'),
    )

    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='works',
                                verbose_name="ایجاد کننده")

    category = models.ManyToManyField(Category,
                                      verbose_name='دسته بندی')  # many to many with Category
    title = models.CharField(max_length=50, verbose_name='نام محصول')
    slug = models.SlugField(max_length=100, unique=True, null=False, verbose_name="آدرس url محصول(slug)")
    keywords = models.CharField(max_length=255, blank=True, verbose_name='کلمات کلیدی')
    description = models.CharField(max_length=255, verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/', verbose_name='تصویر اصلی')
    detail = RichTextUploadingField(verbose_name='جزئیات')
    status = models.CharField(max_length=20, choices=STATUS, verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    objects = WorkManager()

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img style="border-radius: 5px" src="{}" height="75px"/>'.format(self.image.url))

    image_tag.short_description = 'تصویر'

    def category_to_str(self):
        return ", ".join([category.title for category in self.category.filter(status='True')])

    category_to_str.short_description = "دسته بندی"

    class Meta:
        verbose_name = 'نمونه کار'
        verbose_name_plural = 'نمونه کارها'

    def get_absolute_url(self):
        return reverse("works:WorkDetail", kwargs={'slug': self.slug, })

    # def average_review(self):
    #     reviews = Comment.objects.filter(product=self).aggregate(average=Avg('rate'))
    #     avg = 0
    #     if reviews["average"] is not None:
    #         avg = float(reviews["average"])
    #     return avg

    # def counter_view(self):
    #     reviews = Comment.objects.filter(product=self).aggregate(count=Count('id'))
    #     cnt = 0
    #     if reviews["count"] is not None:
    #         cnt = int(reviews["count"])
    #     return cnt

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'

    def status_persian(self):
        if self.status == "True":
            return 'فعال'
        else:
            return 'غیرفعال'


class Gallery(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name='نمونه کار')
    title = models.CharField(max_length=50, blank=True, verbose_name='نام')
    image = models.ImageField(blank=True, upload_to='images/', verbose_name='تصویر')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img style="border-radius: 5px" src="{}" height="75"/>'.format(self.image.url))

    image_tag.short_description = 'تصویر'

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'گالری تصاویر'
