from django.db import models

# Create your models here.

class Museo(models.Model):
    ID_ENTIDAD = models.CharField(max_length=100, default="")
    NOMBRE = models.CharField(max_length=100, default="")
    HORARIO = models.TextField(default="")
    DESCRIPCION_ENTIDAD = models.TextField(default="")
    EQUIPAMIENTO = models.TextField(default="")
    TRANSPORTE = models.TextField(default="")
    DESCRIPCION = models.TextField(default="")
    ACCESIBILIDAD =models.TextField(default="")
    CONTENT_URL = models.URLField(default="")
    NOMBRE_VIA = models.CharField(max_length=100, default="")
    CLASE_VIAL = models.CharField(max_length=100, default="")
    TIPO_NUM = models.CharField(max_length=100, default="")
    NUM = models.TextField(default="")
    PLANTA = models.CharField(max_length=100, default="")
    LOCALIDAD = models.CharField(max_length=100, default="")
    PROVINCIA = models.CharField(max_length=100, default="")
    CODIGO_POSTAL = models.CharField(max_length=100, default="")
    BARRIO = models.CharField(max_length=100, default="")
    DISTRITO = models.CharField(max_length=100, default="")
    COORDENADA_X = models.CharField(max_length=100, default="")
    COORDENADA_Y = models.CharField(max_length=100, default="")
    LATITUD = models.CharField(max_length=100, default="")
    LONGITUD = models.CharField(max_length=100, default="")
    TELEFONO = models.CharField(max_length=100, default="")
    FAX = models.TextField(default="")
    EMAIL = models.TextField(default="")
    TIPO = models.CharField(max_length=100, default="")
    NUM_COMENTS = models.IntegerField( default=0)

    def __str__(self):
        return self.NOMBRE

class Comentario(models.Model):
    MUSEO = models.ForeignKey(Museo)
    USUARIO = models.TextField(default="Null")
    TEXTO = models.TextField(default="Null")
    FECHA = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.TEXTO

class Museo_Usuario(models.Model):
    MUSEO = models.ForeignKey(Museo)
    FECHA = models.TextField(default = "Null")

    def __str__(self):
        return self.MUSEO.NOMBRE

class Pag_Usuario(models.Model):
    USUARIO = models.TextField(default="Null")
    TITULO = models.TextField(default ="Null")
    COLOR = models.TextField(default = "#fff")
    TAMAÑO = models.TextField(default = "100%")
    MUSEOS = models.ManyToManyField(Museo_Usuario)

    def __str__(self):
        return self.TITULO
