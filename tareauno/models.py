from django.db import models


class Payment_Types(models.Model):
    """
    Modelo para mapear métodos de pago
    """
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Payment Type"
        verbose_name_plural = "Payment Types"

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    Modelo para mapear los datos de localización de la estación
    """
    city = models.CharField(max_length=200, db_index=True)
    country = models.CharField(max_length=5, db_index=True)
    latitude = models.FloatField(default=0.00, blank=True, null=True)
    longitude = models.FloatField(default=0.00, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.city, self.country)


class Company(models.Model):
    """
    Modelo para mapear los datos de la compañia
    """
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Network(models.Model):
    """
    Modelo para mapear las caracteristicas principales de la red
    """
    name = models.CharField(max_length=50, db_index=True)
    companies = models.ManyToManyField(Company, blank=True)
    gbfs_href = models.URLField(max_length=500, blank=True, null=True)
    href = models.CharField(max_length=150)
    external_id = models.CharField(max_length=150, db_index=True)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Station(models.Model):
    """
    Modelo para describir cada estación de la red
    """
    name = models.CharField(max_length=50, db_index=True)
    empty_slots = models.PositiveIntegerField(blank=True, null=True)
    free_bikes = models.PositiveIntegerField(blank=True, null=True)
    external_id = models.CharField(max_length=150, db_index=True)
    latitude = models.FloatField(default=0.00, blank=True, null=True)
    longitude = models.FloatField(default=0.00, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    network = models.ForeignKey(Network, blank=True, null=True, on_delete=models.CASCADE)

    # Extra data, también podría modelarse en una relación one2one
    address = models.CharField(max_length=250)
    altitude = models.FloatField(default=0.00, blank=True, null=True)
    ebikes = models.PositiveIntegerField(blank=True, null=True)
    has_ebikes = models.BooleanField(default=False)
    last_updated = models.DateTimeField(blank=True, null=True)
    normal_bikes = models.PositiveIntegerField(blank=True, null=True)
    payment = models.ManyToManyField(Payment_Types, blank=True)
    payment_terminal = models.BooleanField(default=False)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    renting = models.PositiveIntegerField(blank=True, null=True)
    returning = models.PositiveIntegerField(blank=True, null=True)
    slots = models.PositiveIntegerField(blank=True, null=True)
    uid = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name