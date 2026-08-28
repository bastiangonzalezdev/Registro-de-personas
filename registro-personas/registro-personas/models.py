from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Persona(db.Model):
    __tablename__ = "personas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    correo = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"<Persona {self.nombre} {self.apellido}>"
