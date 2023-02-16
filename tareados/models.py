from django.db import models

class Project(models.Model):
    """
    Modelo para describir cada estación de la red
    """
    external_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField("Nombre", max_length=50, db_index=True, blank=True, null=True)
    type = models.CharField("Tipo", max_length=10, db_index=True, blank=True, null=True)
    region = models.CharField("Región", max_length=50, blank=True, null=True)
    typology = models.CharField("Tipología", max_length=5, blank=True, null=True)
    owner = models.CharField("Títular", max_length=50, db_index=True, blank=True, null=True)
    investment = models.FloatField("Inversión MMU$", default=0.00, blank=True, null=True)
    date_income = models.DateField("Fecha Presentación", blank=True, null=True)
    status = models.CharField("Estado", max_length=150, db_index=True, blank=True, null=True)
    
    def __str__(self):
        return self.name
