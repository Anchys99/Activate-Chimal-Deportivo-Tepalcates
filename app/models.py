from .extensions import db


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    apellidos = db.Column(db.String(150), nullable=False)

    correo = db.Column(db.String(150), unique=True, nullable=False)

    contraseña = db.Column(db.String(255), nullable=False)

    edad = db.Column(db.Integer, nullable=True)

    peso = db.Column(db.Float, nullable=True)

    estatura = db.Column(db.Float, nullable=True)

    objetivo = db.Column(db.String(200), nullable=True)

class Actividad(db.Model):

        __tablename__ = "actividades"

        id = db.Column(db.Integer, primary_key=True)

        usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

        actividad = db.Column(db.String(100), nullable=False)

        tiempo = db.Column(db.Integer, nullable=False)

        distancia = db.Column(db.Float, nullable=True)

        calorias = db.Column(db.Float, nullable=True)

        esfuerzo = db.Column(db.String(20), nullable=True)
        
        fecha = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

        
class Novedad(db.Model):
    __tablename__ = "novedades"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=True)
    lugar = db.Column(db.String(150), nullable=True)
    estado = db.Column(db.String(20), default="publicada", nullable=False)
    fecha_publicacion = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        nullable=False
    )


class Personal(db.Model):
    __tablename__ = "personal"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
