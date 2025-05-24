from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Address(models.Model):
    client = models.ForeignKey(
        Client, related_name="addresses", on_delete=models.CASCADE
    )
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    complement = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    nickname = models.CharField(max_length=100)
