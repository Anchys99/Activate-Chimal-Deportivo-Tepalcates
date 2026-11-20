from flask import Blueprint, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import Usuario, Actividad
from datetime import datetime
from zoneinfo import ZoneInfo

usuarios = Blueprint(
    "usuarios",
    __name__,
    url_prefix="/usuarios"
)


@usuarios.route("/")
def inicio_usuarios():
    if "usuario_id" not in session:
        return redirect("/usuarios/login")

    nombre = session.get("usuario_nombre", "Usuario")

    actividades = [
        "Caminar",
        "Correr",
        "Bicicleta",
        "Fútbol",
        "Boxeo",
        "Natación",
        "Atletismo"
    ]

    historial = Actividad.query.filter_by(
        usuario_id=session["usuario_id"]
    ).order_by(Actividad.id.desc()).all()

    return render_template(
        "usuarios/inicio.html",
        nombre=nombre,
        actividades=actividades,
        historial=historial
    )


@usuarios.route("/seleccionar-actividad")
def seleccionar_actividad():
    if "usuario_id" not in session:
        return redirect("/usuarios/login")

    actividades = [
        "Caminar",
        "Correr",
        "Bicicleta",
        "Fútbol",
        "Boxeo",
        "Natación",
        "Atletismo"
    ]

    return render_template(
        "usuarios/seleccionar_actividad.html",
        actividades=actividades
    )



@usuarios.route("/actividad/<actividad>", methods=["GET", "POST"])
def actividad(actividad):
    if "usuario_id" not in session:
        return redirect("/usuarios/login")

    usuario_id = session["usuario_id"]
    usuario = db.session.get(Usuario, usuario_id)

    mensaje = None

    if request.method == "POST":
        deporte = request.form.get("deporte", actividad).strip()
        tiempo_texto = request.form.get("tiempo", "").strip()
        distancia_texto = request.form.get("distancia", "").strip()
        esfuerzo = request.form.get("esfuerzo", "medio")

        if not tiempo_texto:
            mensaje = "Ingresa el tiempo de la actividad."
            return render_template(
                "usuarios/actividad.html",
                actividad=actividad,
                mensaje=mensaje
            )

        try:
            tiempo = int(tiempo_texto)
            distancia = (
                float(distancia_texto)
                if distancia_texto else None
            )

            if tiempo <= 0:
                raise ValueError

            peso = (
                usuario.peso
                if usuario and usuario.peso
                else 70
            )

            valores_met = {
                "Caminar": 3.5,
                "Correr": 8.0,
                "Bicicleta": 6.0,
                "Fútbol": 7.0,
                "Boxeo": 7.0,
                "Natación": 6.0,
                "Atletismo": 7.0
            }

            met = valores_met.get(deporte, 4.0)
            calorias = round(
                met * 3.5 * peso / 200 * tiempo,
                1
            )

        except ValueError:
            mensaje = "Ingresa un tiempo y una distancia válidos."
            return render_template(
                "usuarios/actividad.html",
                actividad=actividad,
                mensaje=mensaje
            )

        nueva_actividad = Actividad(
            usuario_id=usuario_id,
            actividad=deporte,
            tiempo=tiempo,
            distancia=distancia,
            calorias=calorias,
            esfuerzo=esfuerzo,
            fecha=datetime.now(ZoneInfo("America/Mexico_City"))
        )

        db.session.add(nueva_actividad)
        db.session.commit()

        mensaje = "Actividad registrada correctamente"

    return render_template(
        "usuarios/actividad.html",
        actividad=actividad,
        mensaje=mensaje
    )

@usuarios.route("/perfil/editar", methods=["GET", "POST"])


def editar_perfil():

    if "usuario_id" not in session:
        return redirect("/usuarios/login")

    usuario_id = session["usuario_id"]
    usuario = db.session.get(Usuario, usuario_id)

    if usuario is None:
        session.clear()
        return redirect("/usuarios/login")

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        apellidos = request.form.get("apellidos", "").strip()
        correo = request.form.get("correo", "").strip()

        if not nombre or not apellidos or not correo:
            mensaje = "Nombre, apellidos y correo son obligatorios."
            return render_template(
                "usuarios/editar_perfil.html",
                usuario=usuario,
                mensaje=mensaje
            )

        usuario.nombre = nombre
        usuario.apellidos = apellidos
        usuario.correo = correo

        edad = request.form.get("edad")
        peso = request.form.get("peso")
        estatura = request.form.get("estatura")

        usuario.edad = int(edad) if edad else None
        usuario.peso = float(peso) if peso else None
        usuario.estatura = float(estatura) if estatura else None
        usuario.objetivo = request.form.get("objetivo", "").strip()

        db.session.commit()

        return redirect("/usuarios/perfil")

    return render_template(
        "usuarios/editar_perfil.html",
        usuario=usuario
    )


@usuarios.route("/perfil")
def ver_perfil():
    if "usuario_id" not in session:
        return redirect("/usuarios/login")

    usuario_id = session["usuario_id"]
    usuario = db.session.get(Usuario, usuario_id)

    if usuario is None:
        session.clear()
        return redirect("/usuarios/login")

    return render_template(
        "usuarios/perfil.html",
        usuario=usuario
    )


@usuarios.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        edad = request.form.get("edad")
        peso = request.form.get("peso")
        estatura = request.form.get("estatura")
        objetivo = request.form.get("objetivo")

        contraseña_hash = generate_password_hash(contraseña)

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            correo=correo,
            contraseña=contraseña_hash,
            edad=int(edad) if edad else None,
            peso=float(peso) if peso else None,
            estatura=float(estatura) if estatura else None,
            objetivo=objetivo
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return "Usuario registrado correctamente"

    return render_template("registro/registro.html")

@usuarios.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.contraseña, contraseña):

            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre

            return redirect("/usuarios/")

        return "Correo o contraseña incorrectos"

    return render_template("login/login.html")

@usuarios.route("/logout")
def logout():

    session.clear()

    return redirect("/usuarios/login")
