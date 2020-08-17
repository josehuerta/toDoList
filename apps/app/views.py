from django.shortcuts import render,redirect

from django.db.models.query import RawQuerySet
from itertools import chain


from .models import Usuarios,Listas,Tareas,Reelevancias,Estados


#Basically use get() when you want to get a single unique object, 
#and filter() when you want to get all objects that match your lookup parameters.

#hay 2 formas de colocar el valor de una llave foranea
#se hace el ejemplo con el id de usuario en la tabla
#listas 
#1 lista.usuario_id=1
#2 lista.usuario=Usuario.objects.get(id=1)

#en la segunda forma necesitamos la instancia del objeto
#en la primera solo el valor 
def index(request):
    return render(request,'index.html')
def inicio(request):
    nombre='Mi lista'
    id_usuario=request.session['id']
    usuario=Usuarios.objects.get(id=id_usuario)

    #obtenemos todas las listas de ese usuario con ese id
    listas_usuario=Listas.objects.filter(usuario_id=id_usuario)
    
    for lista in listas_usuario:
        if lista.nombre_lista=="Mi lista":
            tareas=Tareas.objects.filter(lista=lista.id)
        else:
            tareas=list(chain(tareas,Tareas.objects.filter(lista=lista.id)))
        
    
    #obtenemos la lista llamada mi lista
    #mi_lista=listas_usuario.get(nombre_lista=nombre)
    mi_lista=Listas.objects.get(usuario_id=id_usuario,nombre_lista=nombre)

    #obtenemos todas las tareas colocadas en la lista mi lista
    mis_tareas=mi_lista.tareas_set.filter(lista_id=mi_lista.id)
    #lista_principal=listas_usuario.tareas_set.filter(nombre_lista=nombre)
    relevancias=Reelevancias.objects.all()
    
    
    for tarea in tareas:
        tarea.fecha_vencimiento=str(tarea.fecha_vencimiento)[0:10]+'T'+str(tarea.fecha_vencimiento)[11:19]

    for tarea in mis_tareas:
        tarea.fecha_vencimiento=str(tarea.fecha_vencimiento)[0:10]+'T'+str(tarea.fecha_vencimiento)[11:19]
    
    contexto={
        'listas':listas_usuario,
        'tareas':tareas,
        'mis_tareas':mis_tareas,
        'relevancias':relevancias,
        'usuario':usuario,
    }

    return render(request,'inicio.html',contexto)

def salir(request):
    return redirect(index)
    
#CRUD USUARIO---------------------------
def crearUsuario(request):
    
    nombre=request.POST.get('nombre')
    apellido=request.POST.get('apellido')
    correo=request.POST.get('email_reg')
    password=request.POST.get('password_reg')
    
    consulta=Usuarios.objects.filter(correo=correo)
    #la consulta dara un len=0 , si no existe un usuario con ese correo

    if len(consulta)==0:
        #creando el nuevo usuario
        nuevo_usuario=Usuarios.objects.create(nombre=nombre,apellidos=apellido,correo=correo,password=password)
        nuevo_usuario.save()
        #a cada nuevo usuario se le creara una lista llamada mi lista
        nombre_lista='Mi lista'
        nueva_lista=Listas.objects.create(nombre_lista=nombre_lista,usuario_id=nuevo_usuario.id)
        nueva_lista.save()

        request.session['id']=nuevo_usuario.id

        return redirect(iniciarSesion)
    
    return redirect(index)

def eliminarUsuario(request,id):
    usuario=Usuarios.objects.get(id=id)
    usuario.delete()
    return redirect(index)

def editarUsuario(request,id):
    usuario=Usuarios.objects.get(id=id)
    password=request.POST['password']
    n_password=request.POST['n_password']

    if usuario.password==password:
        usuario.nombre=request.POST['nombre']
        usuario.apellidos=request.POST['apellido']
        if n_password !="":
            usuario.password=n_password

        usuario.save()

    return redirect(inicio)

#-------------------------------------
def iniciarSesion(request):

    if request.method=='POST':
        #si entramos por POST , significa que le usuario introdujo su correo y password
        email=request.POST.get('email_usr')
        password=request.POST.get('password_usr')

        #query=f"select * from app_usuarios where correo='{email}' and password='{password}'"
        #resultado=Usuarios.objects.raw(query)
        resultado=Usuarios.objects.filter(correo=email)
        if  len(resultado)>0:    
            request.session['id']=resultado[0].id
            return redirect(inicio)

    else:
        #si entramos por GET , es por que venimos de acabar de crear el usuario
        return redirect(crearLista)
    
    return redirect('index')

def cerrarSesion(request):
    pass

#CRUD LISTAS---------------------------------------------------
def crearLista(request):
    id_usuario=request.session['id']
    nombre_lista=""
    if request.method=='POST':
        nombre_lista=request.POST.get('nueva_lista')
    else:
        nombre_lista='Mi lista'
        
    nueva_lista=Listas.objects.create(nombre_lista=nombre_lista,usuario_id=16)    
    nueva_lista.save()

    return redirect(inicio)

def eliminarLista(request,id):
    lista=Listas.objects.get(id=id)
    lista.delete()
    return redirect(inicio)

#CRUD TAREAS----------------------------------------------------
def crearTarea(request):

    if request.method=='POST':
        #https://es.stackoverflow.com/questions/30744/cannot-assign-1-cliente-tipo-cliente-must-be-a-tipocliente-instance
        tarea=request.POST.get('tarea')
        fechaVencimiento=request.POST.get('fecha')
        relevancia=request.POST.get('relevancia')
        lista=request.POST.get('lista')
        estado=1
        nueva_tarea=Tareas()
        nueva_tarea.tarea=tarea
        nueva_tarea.fecha_vencimiento=fechaVencimiento
        nueva_tarea.estado_id=estado
        nueva_tarea.lista_id=lista
        nueva_tarea.reelevancia_id=relevancia
        
        
        nueva_tarea.save()

    return redirect(inicio)

def eliminarTarea(request,id):

    tarea=Tareas.objects.get(id=id)
    tarea.delete()
    return redirect(inicio)

def editarTarea(request,id):
    tarea=Tareas.objects.get(id=id)
    tarea.tarea=request.POST.get('tarea_ed')
    print("hola",request.POST.get('tarea_ed'))
    tarea.fecha_vencimiento=request.POST.get('fecha_ed')
    tarea.reelevancia_id=request.POST.get('relevancia_ed')
    tarea.save()
    return redirect(inicio)


    