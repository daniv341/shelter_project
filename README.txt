==============================================================
SISTEMA DE GESTIÓN DE REFUGIO DE ANIMALES - README
==============================================================

Proyecto Django + Django REST Framework + PostgreSQL, con
arquitectura en capas (models / serializers / views / services /
repositories / selectors) y documentación automática vía
drf-spectacular (Swagger UI).

--------------------------------------------------------------
1. REQUISITOS
--------------------------------------------------------------
- Python 3.13+ (probado también con 3.12)
- PostgreSQL 14+ corriendo localmente o accesible por red
- pip

--------------------------------------------------------------
2. CÓMO LEVANTAR UN ENTORNO VIRTUAL EN PYTHON (breve)
--------------------------------------------------------------
Desde la raíz del proyecto:

    python3 -m venv venv

Activar el entorno:
    - Linux/Mac:   source venv/bin/activate
    - Windows:     venv\Scripts\activate

Para salir del entorno virtual, en cualquier momento:
    deactivate

--------------------------------------------------------------
3. INSTALACIÓN DE DEPENDENCIAS
--------------------------------------------------------------
Con el entorno virtual activado:

    pip install -r requirements.txt

--------------------------------------------------------------
4. VARIABLES DE ENTORNO (.env)
--------------------------------------------------------------
Se incluye un archivo ".env.example" con variables de ejemplo.
Copiarlo a ".env" y ajustar los valores según tu entorno:

    cp .env.example .env

Variables principales:
    DJANGO_SECRET_KEY          -> clave secreta de Django
    DJANGO_DEBUG                -> True/False
    DJANGO_ALLOWED_HOSTS        -> hosts permitidos, separados por coma
    DB_ENGINE                   -> motor de base de datos
    DB_NAME / DB_USER / DB_PASSWORD / DB_HOST / DB_PORT -> credenciales de PostgreSQL
    JWT_ACCESS_TOKEN_LIFETIME_MINUTES / JWT_REFRESH_TOKEN_LIFETIME_DAYS
        -> configuración de Simple JWT (la autenticación se activará
           más adelante; por ahora los endpoints son de acceso libre)

Antes de levantar el proyecto, asegurate de tener una base de datos
PostgreSQL creada con esos datos, por ejemplo:

    psql -U postgres -c "CREATE DATABASE shelter_db;"
    psql -U postgres -c "CREATE USER shelter_user WITH PASSWORD 'shelter_password';"
    psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE shelter_db TO shelter_user;"

--------------------------------------------------------------
5. MIGRACIONES
--------------------------------------------------------------
Antes de migrar, asegurate de:
    - Tener el entorno virtual activado.
    - Tener el archivo .env configurado apuntando a tu PostgreSQL
      (ver paso 4).
    - Tener la base de datos y el usuario ya creados en PostgreSQL
      (Django no crea la base de datos por vos, solo las tablas).

5.1. Generar migraciones
Las migraciones del modelo Animal ya están incluidas en
animals/migrations/. Solo necesitás generar nuevas migraciones si
modificás algún modelo (agregar/quitar campos, cambiar tipos, etc.):

    python manage.py makemigrations

Esto crea un nuevo archivo en animals/migrations/ describiendo el
cambio. Podés generar migraciones de una app puntual indicando su
nombre:

    python manage.py makemigrations animals

5.2. Aplicar migraciones a la base de datos
Este es el paso obligatorio la primera vez que levantás el proyecto,
y cada vez que haya migraciones nuevas (propias o de Django/DRF):

    python manage.py migrate

Esto crea/actualiza todas las tablas necesarias (las de Animal, más
las de Django: auth, admin, sessions, etc.).

5.3. Ver el estado de las migraciones
Para revisar qué migraciones existen y cuáles ya se aplicaron
(marcadas con [X]) o faltan aplicar (marcadas con [ ]):

    python manage.py showmigrations

5.4. Ver el SQL de una migración (opcional)
Si querés inspeccionar qué SQL va a ejecutar una migración antes de
aplicarla:

    python manage.py sqlmigrate animals 0001

5.5. Revertir una migración (opcional)
Para deshacer migraciones y volver la app "animals" a un estado
anterior (por ejemplo, al estado previo a que existiera cualquier
tabla), indicá el nombre de la app y el número de la migración
destino. "zero" revierte todas las migraciones de esa app:

    python manage.py migrate animals zero

Para volver a un punto intermedio, usá el nombre de esa migración:

    python manage.py migrate animals 0001

5.6. Notas
    - Cada vez que hagas pull de cambios que incluyan nuevas
      migraciones (de este proyecto o de una librería), corré de
      nuevo "python manage.py migrate" antes de levantar el server.
    - "makemigrations" solo genera el archivo de migración; no toca
      la base de datos. El que efectivamente crea/modifica tablas es
      "migrate".

--------------------------------------------------------------
6. LEVANTAR Y EJECUTAR EL PROYECTO
--------------------------------------------------------------
1. Activar el entorno virtual.
2. Instalar dependencias (paso 3).
3. Configurar el archivo .env (paso 4) apuntando a tu PostgreSQL.
4. Ejecutar migraciones (paso 5).
5. (Opcional) Crear un superusuario para acceder al admin:

       python manage.py createsuperuser

6. Levantar el servidor de desarrollo:

       python manage.py runserver

7. La API quedará disponible en:

       http://127.0.0.1:8000/api/animals/

   Documentación interactiva (Swagger UI):

       http://127.0.0.1:8000/api/docs/

   Esquema OpenAPI (JSON/YAML):

       http://127.0.0.1:8000/api/schema/

   Panel de administración de Django:

       http://127.0.0.1:8000/admin/

--------------------------------------------------------------
7. EJECUTAR LAS PRUEBAS
--------------------------------------------------------------
El proyecto usa pytest + pytest-django. Con el entorno virtual
activado y el .env configurado:

    pytest

Esto ejecuta:
    - animals/tests/test_domain.py   -> pruebas de dominio
      (repository, selector y service, sin pasar por HTTP)
    - animals/tests/test_endpoints.py -> pruebas de los endpoints
      REST (list, retrieve, create, update, delete)

Nota: pytest-django crea y destruye automáticamente una base de
datos de pruebas separada; no es necesario crearla a mano, pero sí
necesita poder conectarse al motor configurado en DB_ENGINE/.env
(por defecto, PostgreSQL) con permisos para crear bases de datos.

--------------------------------------------------------------
8. QUÉ HACE CADA ARCHIVO
--------------------------------------------------------------

Raíz del proyecto
    manage.py            -> Utilidad de línea de comandos de Django.
    requirements.txt      -> Dependencias del proyecto.
    .env.example / .env   -> Variables de entorno (ejemplo y real).
    pytest.ini             -> Configuración de pytest-django.
    README.txt            -> Este archivo.

config/ (configuración global del proyecto)
    settings.py    -> Configuración de Django, DRF, drf-spectacular,
                      Simple JWT y base de datos, leída desde .env.
    urls.py        -> URLs raíz: admin, API de animals, schema
                      OpenAPI y Swagger UI.
    wsgi.py / asgi.py -> Puntos de entrada para servidores WSGI/ASGI.

animals/ (módulo de gestión de animales)
    models.py         -> Entidad Animal (ORM), con ULID como PK y
                          TextChoices para sexo, estado de adopción
                          y estado médico. Sin lógica de negocio.
    serializers.py     -> AnimalReadSerializer (salida completa) y
                          AnimalWriteSerializer (entrada para
                          create/update). Validación y forma de los
                          datos que entran/salen de la API.
    views.py           -> AnimalViewSet: vista delgada (ModelViewSet
                          basado en mixins) que solo valida el
                          serializer y delega al AnimalService.
                          Documentada con @extend_schema /
                          @extend_schema_view para Swagger.
    services.py         -> AnimalService: lógica de negocio, coordina
                          AnimalRepository (escritura) y
                          AnimalSelector (lectura). Punto de
                          extensión para reglas de negocio futuras.
    repositories.py     -> AnimalRepository: únicas operaciones de
                          escritura sobre la base de datos
                          (create/update/delete).
    selectors.py        -> AnimalSelector: únicas operaciones de
                          lectura (get_by_id/get_all).
    filters.py           -> AnimalFilter (django-filter): filtros de
                          listado por species, name, sex,
                          adoption_status y medical_status.
    permissions.py       -> Permisos personalizados. Por ahora el
                          acceso es libre (AllowAny); se deja
                          IsStaffOrReadOnly lista para cuando se
                          active la autenticación JWT.
    admin.py             -> Configuración del Django Admin para
                          Animal (list_display, filtros, búsqueda).
    apps.py              -> Configuración de la app Django.
    urls.py              -> Rutas de la API de animals (DefaultRouter
                          -> /api/animals/, /api/animals/{id}/).
    migrations/           -> Migraciones generadas por Django.
    tests/
        test_domain.py    -> Pruebas de repository, selector y
                          service (sin HTTP).
        test_endpoints.py -> Pruebas de los endpoints REST (con
                          APIClient de DRF).
