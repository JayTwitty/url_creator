from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class URL(models.Model):
    input_url = models.URLField()
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    output_url = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)


    def __str__(self):
        return "{}, {}".format(self.input_url, self.output_url)

    class Meta:
        ordering = ["-timestamp"]


    @property
    def click_count(self):
        return self.click_set.all().count()


class Click(models.Model):
    clicked = models.BooleanField(default=True)
    url = models.ForeignKey(URL)