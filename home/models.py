from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe

from extensions.utils import jalali_converter


class Setting(models.Model):
    STATUS = (
        ('True', 'فعال'),
        ('False', 'غیرغعال'),
    )
    title = models.CharField(max_length=150, verbose_name='عنوان وب سایت')
    keywords = models.CharField(max_length=255, verbose_name='کلمات کلیدی')
    description = models.CharField(max_length=255, verbose_name='توضیحات')
    company = models.CharField(blank=True, max_length=50, verbose_name='شرکت')
    address = models.CharField(blank=True, max_length=255, verbose_name='آدرس')
    phone = models.CharField(blank=True, max_length=20,
                             verbose_name="تلفن همراه (جهت دریافت اطلاع رسانی پیامکی وبسایت)")
    phone2 = models.CharField(blank=True, max_length=20, verbose_name='شماره تماس ثابت')
    fax = models.CharField(blank=True, max_length=20, verbose_name='فکس')
    email = models.CharField(blank=True, max_length=70, verbose_name='ایمیل')

    icon = models.ImageField(upload_to='images/', verbose_name='لوگو'
                             , help_text='لوگو اصلی نمایش در بالای سایت')
    shortcut_icon = models.ImageField(blank=True, upload_to='images/', verbose_name='لوگو کوچک',
                                      help_text='نسبت 1.1 به منظور نمایش در تب مرورگر')
    facecbook = models.CharField(blank=True, max_length=100, verbose_name='فیسبوک')
    instagram = models.CharField(blank=True, max_length=100, verbose_name='اینستاگرام')
    telegram = models.CharField(blank=True, max_length=100, verbose_name='تلگرام')
    youtube = models.CharField(blank=True, max_length=100, verbose_name='یوتیوب')
    twitter = models.CharField(blank=True, max_length=100, verbose_name='توییتر')
    linkedin = models.CharField(blank=True, max_length=100)
    aboutme1 = models.TextField(blank=True, verbose_name='درباره من 1')
    aboutme2 = RichTextUploadingField(blank=True, verbose_name='درباره من 2')
    contact = RichTextUploadingField(blank=True, verbose_name='تماس با ما')
    worktime = RichTextUploadingField(blank=True, verbose_name='ساعت کاری')
    customerservices = RichTextUploadingField(blank=True, verbose_name='خدمات مشتریان')
    notices = RichTextUploadingField(blank=True, verbose_name="اعلامیه وبسایت")
    status = models.CharField(max_length=20, choices=STATUS, verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __String__(self):
        return self.title

    class Meta:
        verbose_name = 'اطلاعات وب سایت'
        verbose_name_plural = 'اطلاعات سایت'

    def j_date(self):
        return jalali_converter(self.create_at)

    j_date.short_description = 'تاریخ'

    def get_absolute_url(self):
        return reverse("home:AboutMe")


class SlideshowManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Slideshow(models.Model):
    # description = models.CharField(blank=True, max_length=255, verbose_name="توضیحات")
    image = models.ImageField(upload_to='images/', verbose_name="تصویر", )
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    # page_url = models.URLField(max_length=200, verbose_name="آدرس")
    ordering_position = models.IntegerField(verbose_name="ترتیب نمایش اسلاید")

    objects = SlideshowManager()

    def __str__(self):
        return " # " + str(self.ordering_position)


    def image_tag(self):
        return mark_safe('<img style="border-radius: 5px" src="{}" height="75"/>'.format(self.image.url))

    image_tag.short_description = "تصویر"

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلایدشو'
        ordering = ["ordering_position"]
