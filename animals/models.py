from django.db import models

# Create your models here.
# class Contributor(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()

#     def __str__(self):
#         return self.name

class Page(models.Model):
    name = models.CharField(max_length=150)
    updated = models.DateTimeField(auto_now=True)

    home_page_views = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

class Animal(models.Model):
    name = models.CharField(max_length=150)
    kingdom = models.CharField(max_length=60)
    phylum = models.CharField(max_length=60)
    classname = models.CharField(max_length=60)
    order = models.CharField(max_length=60)
    family = models.CharField(max_length=60)
    genus = models.CharField(max_length=60)
    scientificname = models.CharField(max_length=150)
    profile_views = models.IntegerField(default=0, null=True, blank=True)

    # image = models.ImageField(null=True, blank=True)


    # contributor = models.ForeignKey('Contributor', related_name='animals', on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name_plural = 'Animals'   # to define plural 

    def __str__(self):
        return self.name