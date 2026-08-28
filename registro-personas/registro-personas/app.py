from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Persona

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///personas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "cambia-esta-clave-por-una-segura"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    personas = Persona.query.order_by(Persona.id).all()
    return render_template("index.html", personas=personas)


@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        edad = request.form.get("edad", "").strip()
        correo = request.form.get("correo", "").strip()

        if not nombre or not apellido or not edad:
            flash("Nombre, apellido y edad son obligatorios.")
            return redirect(url_for("agregar"))

        try:
            edad = int(edad)
        except ValueError:
            flash("La edad debe ser un número.")
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
        persona.nombre = request.form.get("nombre", "").strip()
        persona.apellido = request.form.get("apellido", "").strip()
        correo = request.form.get("correo", "").strip()
        edad = request.form.get("edad", "").strip()

        try:
            persona.edad = int(edad)
        except ValueError:
            flash("La edad debe ser un número.")
            return redirect(url_for("editar", persona_id=persona_id))

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
    app.run(debug=True)
