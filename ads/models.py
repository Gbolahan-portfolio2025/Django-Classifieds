from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    class Meta:
        verbose_name_plural ='Categories'

    def __str__(self):
        return self.name
    

class Ad(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.Draft)
    owner = models.ForeignKey(settings.AUTH_User_MODEL, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('change_ad', 'Can change this ad'),
            ('delete_ad', 'Can delete this ad'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Ad.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
