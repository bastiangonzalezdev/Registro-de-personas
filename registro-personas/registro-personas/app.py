import os

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Persona

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///personas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave-por-una-segura")

db.init_app(app)

with app.app_context():
    db.create_all()


def validar_datos(nombre, apellido, edad_raw):
    """Valida los campos del formulario y devuelve (edad_int, error)."""
    if not nombre or not apellido or not edad_raw:
        return None, "Nombre, apellido y edad son obligatorios."

    try:
        edad = int(edad_raw)
    except ValueError:
        return None, "La edad debe ser un número."

    if edad < 0 or edad > 130:
        return None, "La edad debe ser un valor válido."

    return edad, None


@app.route("/")
def index():
    personas = Persona.query.order_by(Persona.id).all()
    return render_template("index.html", personas=personas)


@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        edad_raw = request.form.get("edad", "").strip()
        correo = request.form.get("correo", "").strip() or None

        edad, error = validar_datos(nombre, apellido, edad_raw)
        if error:
            flash(error)
            return redirect(url_for("agregar"))

        nueva_persona = Persona(
            nombre=nombre, apellido=apellido, edad=edad, correo=correo
        )
        db.session.add(nueva_persona)
        db.session.commit()
        flash("Persona agregada correctamente.")
        return redirect(url_for("index"))

    return render_template("formulario.html", persona=None)


@app.route("/editar/<int:persona_id>", methods=["GET", "POST"])
def editar(persona_id):
    persona = Persona.query.get_or_404(persona_id)

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        edad_raw = request.form.get("edad", "").strip()
        correo = request.form.get("correo", "").strip() or None

        edad, error = validar_datos(nombre, apellido, edad_raw)
        if error:
            flash(error)
            return redirect(url_for("editar", persona_id=persona_id))

        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = edad
        persona.correo = correo
        db.session.commit()
        flash("Persona actualizada correctamente.")
        return redirect(url_for("index"))

    return render_template("formulario.html", persona=persona)


@app.route("/eliminar/<int:persona_id>", methods=["POST"])
def eliminar(persona_id):
    persona = Persona.query.get_or_404(persona_id)
    db.session.delete(persona)
    db.session.commit()
    flash("Persona eliminada correctamente.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "1") == "1")
