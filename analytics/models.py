from django.db import models
from localflavor.us.models import USStateField


class Page(models.Model):
    url = models.URLField(unique=True)

    def __unicode__(self):
        return u"{}".format(self.url)


class Location(models.Model):
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    region = models.CharField(max_length=20)

    class Meta:
        unique_together = (("city", "country", "region"),)

    def __unicode__(self):
        return u"{}".format(self.city)


class View(models.Model):
    ip_address = models.CharField(max_length=30, blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(Page, related_name="views")
    location = models.ForeignKey(Location, related_name="views", blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return u"{}, {}, {}".format(self.page, self.ip_address, self.date_time)


class Ad(models.Model):
    image = models.ImageField(upload_to='ads')
    url = models.URLField()
    state = USStateField()

    def __unicode__(self):
        return u"{}, {}".format(self.state, self.url)