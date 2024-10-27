from django.db import models

class ServiceProvider(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    contact_info = models.CharField(max_length=255)
    clicks = models.IntegerField(default=0)
    impressions = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class ServiceProviderImage(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.service_provider.name}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'SubCategories'
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    file = models.FileField(upload_to='services/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

from django.contrib.auth.models import User

class PendingService(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='pending_services/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)  # Flag 
