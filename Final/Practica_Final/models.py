from django.db import models

# Create your models here.

class Museo(models.Model):
    ID_ENTIDAD = models.CharField(max_length=100, default="Null")
    NOMBRE = models.CharField(max_length=100, default="Null")
    HORARIO = models.TextField(default="Null")
    DESCRIPCION_ENTIDAD = models.TextField(default="Null")
    EQUIPAMIENTO = models.TextField(default="Null")
    TRANSPORTE = models.TextField(default="Null")
    DESCRIPCION = models.TextField(default="Null")
    ACCESIBILIDAD =models.TextField(default="Null")
    CONTENT_URL = models.URLField(default="Null")
    NOMBRE_VIA = models.CharField(max_length=100, default="Null")
    CLASE_VIAL = models.CharField(max_length=100, default="Null")
    TIPO_NUM = models.CharField(max_length=100, default="Null")
    NUM = models.TextField(default="Null")
    PLANTA = models.CharField(max_length=100, default="Null")
    LOCALIDAD = models.CharField(max_length=100, default="Null")
    PROVINCIA = models.CharField(max_length=100, default="Null")
    CODIGO_POSTAL = models.CharField(max_length=100, default="Null")
    BARRIO = models.CharField(max_length=100, default="Null")
    DISTRITO = models.CharField(max_length=100, default="Null")
    COORDENADA_X = models.CharField(max_length=100, default="Null")
    COORDENADA_Y = models.CharField(max_length=100, default="Null")
    LATITUD = models.CharField(max_length=100, default="Null")
    LONGITUD = models.CharField(max_length=100, default="Null")
    TELEFONO = models.CharField(max_length=100, default="Null")
    FAX = models.TextField(default="Null")
    EMAIL = models.TextField(default="Null")
    TIPO = models.CharField(max_length=100, default="Null")

    def __str__(self):
        return self.NOMBRE

class Comentario(models.Model):
    MUSEO = models.ForeignKey(Museo)
    USUARIO = models.TextField(default="Null")
    TEXTO = models.TextField(default="Null")
    FECHA = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.TEXTO

class Pag_Usuario(models.Model):
    Usuario = models.CharField(max_length=100, default="Null")
    Museos = models.OneToManyField(Museo)
