from flask import render_template, request,send_from_directory,session,redirect,url_for,flash
from models.guia import NombreGuia
from models.instructor import Instructor
from models.programasFormacion import Programa
from app import app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import traceback


UPLOAD_FOLDER = 'uploads/pdf'


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/listarguia", methods=["GET"])
def listar_guias():
        guias = NombreGuia.objects()
        return render_template("listarguia.html", guias=guias)

@app.route("/agregarguia", methods=['GET', 'POST'])
def agregar_guia():
        mensaje = None
        estado = False
        instructores = Instructor.objects()
        programa = Programa.objects()
        if request.method == 'POST':
            try:
                if 'documento' not in request.files:
                    mensaje = "No se ha cargado ningún archivo PDF."
                    return render_template("agregarguia.html", mensaje=mensaje, estado=estado, instructores=instructores)
                documento = request.files['documento']
                if documento.filename == '':
                    mensaje = "No seleccionaste un archivo PDF."
                    return render_template("agregarguia.html", mensaje=mensaje, estado=estado, instructores=instructores)
                if documento and allowed_file(documento.filename):
                    filename = secure_filename(documento.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    documento.save(filepath)
                    nombreguia = request.form.get("nombreguia")
                    descripcions = request.form.get("descripcions")
                    programa_id = request.form.get("programaformacion")
                    programa_ref = Programa.objects(id=programa_id).first()
                    fecha_str = request.form.get("fecha")
                    fecha=datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else None
                    instructor_id = request.form.get("intructordeproceso")
                    instructor_ref = Instructor.objects(id=instructor_id).first()
                    if instructor_ref:
                        nueva_guia = NombreGuia(
                            nombreguia=nombreguia,
                            descripcions=descripcions,
                            programaformacion=programa_ref.nombre,
                            programa=programa_ref,
                            documento=filename,
                            fecha=fecha,
                            intructordeproceso=instructor_ref
                        )
                        nueva_guia.save()
                        estado = True
                        mensaje = "Guía registrada exitosamente."
                    else:
                        mensaje = "Instructor no encontrado."
                else:
                    mensaje = "El archivo no es un PDF válido."
            except Exception as e:
                import traceback
                print("Error real al guardar la guía:")
                traceback.print_exc()
                mensaje = f"Error al guardar la guía: {str(e)}"
        return render_template("agregarguia.html", mensaje=mensaje, estado=estado, instructores=instructores,programa=programa)


@app.route('/uploads/pdf/<path:filename>')
def download_file(filename):
    return send_from_directory('uploads/pdf', filename)


@app.route("/agregarprograma/",methods=['GET', 'POST'])
def AgregarElPrograma():
    try:
        mensaje=None
        estado=False
        if request.method=='POST':
            datos=request.get_json(force=True)
            genero=programa(**datos)
            genero.save()
            estado=True
            mensaje="Sena Agregado correctamente"
        else:
            mensaje="No permitido"
    except Exception as error:
        mensaje=str(error)
    return render_template('agregarprograma.html',estado=estado,mensaje=mensaje)