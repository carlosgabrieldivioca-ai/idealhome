from django.db import models


class Property(models.Model):
    title = models.CharField(max_length=500)
    address = models.CharField(max_length=500, blank=True)
    district = models.CharField(max_length=100, blank=True)
    municipality = models.CharField(max_length=150, blank=True)
    parish = models.CharField(max_length=250, blank=True)
    location = models.CharField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    typology = models.CharField(max_length=50, blank=True)
    bathrooms = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    features = models.TextField(blank=True)
    gallery = models.TextField(blank=True)
    source_link = models.URLField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def images(self):
        return [x.strip() for x in self.gallery.split(",") if x.strip()]

    def __str__(self):
        return self.title
