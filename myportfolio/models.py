from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    problem_statement = models.TextField()
    business_case = models.TextField()
    solution =  models.TextField()
    view_code_url = models.CharField(max_length=100)
    img_url = models.URLField(default="https://i.pinimg.com/736x/a8/08/35/a808353507aa0bd01a6812a412240758.jpg'")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    
class Aboutme(models.Model):
    content = models.TextField()

class Skills(models.Model):
    skill_name = models.CharField(max_length=100)
    percentage = models.PositiveBigIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.skill_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.skill_name

class Technical_Skills(models.Model):
    skill_category = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.skill_category)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.skill_category

class Professional_Experience(models.Model):
    role = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    joining_date =  models.DateField()
    leaving_date = models.DateField(null=True, blank=True)
    details = models.TextField()
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.role)
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.role
