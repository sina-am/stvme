from django.db import models


class Language(models.Model):
    """ Languages that are supported for translation source and target"""
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'languages'

    def __str__(self):
        return self.name

    
class SpecializedField(models.Model):
    """ Specialized fields for translator who translate text"""
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'specialized_fields'

    def __str__(self):
        return self.name