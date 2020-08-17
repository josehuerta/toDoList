from django.db import models

# Create your models here.

class Usuarios(models.Model):
    nombre=models.CharField(max_length=20,null=False,blank=False)
    apellidos=models.CharField(max_length=20,null=False,blank=False)
    password=models.CharField(max_length=25, null=False,blank=False)
    correo=models.EmailField(null=False,blank=False)

class Listas(models.Model):
    nombre_lista=models.CharField(max_length=30)
    usuario=models.ForeignKey(Usuarios,on_delete=models.CASCADE,null=False,blank=False)

class Reelevancias(models.Model):
    reelevancia_tipo=models.CharField(max_length=20)
    #normal,importante,urgente,finalizado
class Estados(models.Model):
    estado_tipo=models.CharField(max_length=20)
    #pendiente, finalizado


class Tareas(models.Model):
    tarea=models.CharField(max_length=200)
    fecha_vencimiento=models.DateTimeField()
    
    estado=models.ForeignKey(Estados,on_delete=models.CASCADE,null=False,blank=False)
    reelevancia=models.ForeignKey(Reelevancias,on_delete=models.CASCADE,null=False,blank=False)
    
    lista=models.ForeignKey(Listas,on_delete=models.CASCADE,null=False, blank=False)
    


