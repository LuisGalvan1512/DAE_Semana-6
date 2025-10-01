# 📚 Quiz API con Django REST Framework

Este proyecto implementa una API de **quizzes** utilizando Django y Django REST Framework (DRF).  
Permite crear quizzes, preguntas, opciones de respuesta y validar respuestas de usuarios.

---

## 📖 Descripción del Proyecto
- Gestión de **quizzes** con preguntas y opciones.
- Soporte para **múltiples opciones** por pregunta.
- Endpoint para validar respuestas de los usuarios.
- API construida con Django REST Framework y lista para integrarse con apps web/móviles.

---

## 🛠️ Tecnologías Utilizadas
- [Python 3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- SQLite (base de datos por defecto)

---

## ⚙️ Instalación y Ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/LuisGalvan1512/DAE_Semana-6.git
cd DAE_Semana-6
2️⃣ Crear y activar entorno virtual
bash
Copiar código
python -m venv venv
# Activar en Windows
venv\Scripts\activate
# Activar en Linux/Mac
source venv/bin/activate
3️⃣ Instalar dependencias
bash
Copiar código
pip install -r requirements.txt
4️⃣ Migrar base de datos
bash
Copiar código
python manage.py migrate
5️⃣ Crear superusuario (opcional, para admin)
bash
Copiar código
python manage.py createsuperuser
6️⃣ Ejecutar el servidor
bash
Copiar código
python manage.py runserver
📡 Endpoints principales
Panel Admin:
http://127.0.0.1:8000/admin/

Lista y creación de quizzes:
http://127.0.0.1:8000/api/v1/quizzes/

Detalle de un quiz:
http://127.0.0.1:8000/api/v1/quizzes/<id>/

Validar respuesta:
http://127.0.0.1:8000/api/v1/quizzes/<id>/validate/
(Método POST con question_id y choice_id en el body)

🖼️ Capturas de Pantalla
(Agrega aquí screenshots de tu API funcionando en el navegador DRF o en Postman)

🙌 Autor
Luis Enrique Galvan Morales