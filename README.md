# sitio-api

API del sitio personal, desarrollada con Flask y orientada a contenido, internacionalización y servicios para el frontend.

## Objetivo

`Sitio-api` constituye la capa de backend del sitio personal.

Su función es procesar, normalizar, validar y exponer contenido para el frontend, manteniendo separadas la lógica de la aplicación, las fuentes de datos, los contratos de datos y la capa de presentación.

El sistema será utilizado por un frontend independiente publicado mediante GitHub Pages.

## Arquitectura

El proyecto forma parte de una arquitectura separada entre frontend y backend.

```text
Frontend
GitHub Pages
      |
      | HTTPS
      V
sitio-api
Flask
      |
      V
Contenido, servicios y fuentes de datos
```

Durante el desarrollo local, la API puede ser ejecutada mediante Docker y expuesta a través de la dirección IP del equipo anfitrión.

```text
IP del equipo
      |
      V
Docker
      |
      V
Gunicorn
      |
      V
Flask
```

La arquitectura de despliegue utiliza `GitHub Container Registry` para almacenar la imagen de forma privada y `Northflank Developer Sandbox` para ejecutar el contenedor.

```text
Código fuente
GitHub
      |
      V
Construcción Docker
      |
      V
Imagen privada
GitHub Container Registry
      |
      V
Contenedor
Northflank
      |
      +-- Variables de entorno
      +-- Archivo de configuración privado
```

La API utiliza contratos de datos definidos mediante Pydantic y genera su especificación OpenAPI a partir de las rutas y modelos registrados en la aplicación.

```text
Flask
  |
  +-- OpenAPI
  |       |
  |       +-- Rutas de la API
  |       +-- Validación de respuestas
  |       +-- Especificación OpenAPI
  |
  +-- Pydantic
  |       |
  |       +-- Modelos
  |       +-- Contratos de datos
  |
  +-- Swagger UI
          |
          +-- Documentación interactiva
```

## Artefactos y sus permisos

Hay una relación de qué partes del proyecto son públicas y qué partes son privadas:

| Artefactos                  | Permiso                     |
| --------------------------- | --------------------------- |
| Repositorio del proyecto    | Público en GitHub           |
| Imagen OCI                  | Privada en GHCR             |
| Archivo profile-config.json | Privado en Northflank       |
| Servicio HTTPS de API       | Público en Internet         |

La tabla diferencia:
- El repositorio del proyecto es público. Cualquiera puede consultar el código fuente en GitHub.  

- La Open Container Initiative Image (imagen OCI) es el paquete ejecutable construido mediante Docker. Está almacenada privadamente en GitHub Container Registry (GHCR), por lo que solamente identidades autorizadas, como Northflank o el proprietário de la cuenta, pueden descargarla.  

- Northflank almacena profile-config.json privadamente y lo monta como archivo físico dentro del contenedor durante la ejecución.  

- El servicio HTTPS es público porque Northflank expone la API mediante una dirección accesible desde Internet, siendo posible la solicitud mediante `curl`, `PowerShell` u otros clientes HTTP.  


## Tecnologías

El backend utiliza `Python` y `Flask`. `Gunicorn` constituye el servidor WSGI de la aplicación en el contenedor.

`Flask-CORS` controla el origen autorizado para acceder a la API. `Pydantic` define y valida los contratos de datos. `Flask-OpenAPI` genera la especificación `OpenAPI` y proporciona la documentación interactiva mediante `Swagger UI`.

Docker proporciona un entorno común para el desarrollo local y el despliegue. La imagen de producción es almacenada de forma privada en GitHub Container Registry y ejecutada mediante Northflank.
Las herramientas de desarrollo incluyen `Ruff`, `isort`, `pytest` y `pytest-cov` para el formato, la organización de imports, las pruebas automatizadas y la cobertura de código.

Las dependencias son declaradas mediante `pyproject.toml`. Los archivos `requirements.txt` y `requirements_dev.txt` son mantenidos adicionalmente por motivos de compatibilidad con herramientas y automatizaciones existentes.

## Estructura del proyecto

La estructura actual del código principal es:

```text
sitio-api/
|
+-- app.py
+-- api/
|   +-- v1/
|       +-- errors/
|       |   +-- handlers.py
|       |
|       +-- routes/
|           +-- root.py
|           +-- health.py
|           +-- profile.py
|
+-- schemas/
|   +-- base.py
|   +-- responses.py
|   +-- profile.py
|
+-- utils/
|   +-- utils.py
|
+-- tests/
|   +-- conftest.py
|   +-- test_app.py
|   +-- api/
|   |   +-- v1/
|   |       +-- errors/
|   |       |   +-- test_handlers.py
|   |       |
|   |       +-- routes/
|   |           +-- test_root.py
|   |           +-- test_health.py
|   |           +-- test_profile.py
|   |
|   +-- schemas/
|   |   +-- test_profile_schema.py
|   |   +-- test_responses.py
|   |
|   +-- utils/
|       +-- test_utils.py
|
+-- Docs/
|   +-- mapeo_contenido_sitio.md
|
+-- .github/
|   +-- workflows/
|       +-- Integración y promoción de sitio-api desde dev.yml
|
+-- pyproject.toml
+-- Dockerfile
+-- .dockerignore
+-- .gitignore
+-- LICENSE
+-- README.md
```

`app.py` constituye el punto de entrada de la aplicación. Es responsable de crear la aplicación, configurar CORS, registrar las rutas y los manejadores de errores, generar la documentación y redirigir la raíz hacia la versión actual de la API.

## API

La API es versionada desde su primera versión y utiliza `OpenAPI 3.1.0` para describir formalmente sus operaciones, respuestas y schemas.

Actualmente están disponibles:

```text
/
=> redirección hacia /api/v1/

/api/v1/
=> raíz de la versión actual

/api/v1/health/
=> comprobación de estado de la API

/api/v1/{lang}/profile/
=> perfil correspondiente al idioma solicitado

/api/v1/openapi.json
=> especificación OpenAPI de la API

/api/v1/docs/
=> documentación de la API

/api/v1/docs/swagger
=> interfaz Swagger UI

/api/v1/docs/openapi.json
=> especificación utilizada por la documentación
```

La versión `v1` mantiene separadas sus rutas y sus manejadores de errores. Las rutas registradas por la aplicación son incorporadas automáticamente a la especificación OpenAPI y documentan sus posibles respuestas mediante modelos Pydantic.

Actualmente se utilizan contratos específicos para respuestas satisfactorias, datos del perfil y errores HTTP.

```text
OkResponse
=> respuesta satisfactoria

ProfileResponse
=> respuesta satisfactoria con datos del perfil

NotFoundResponse
=> recurso no encontrado

InternalServerErrorResponse
=> error interno del servidor
```

Los errores HTTP `404 Not Found` y `500 Internal Server Error` disponen de respuestas JSON propias. Sus manejadores son registrados globalmente por la aplicación.

Las respuestas siguen una estructura común:

```json
{
    "status": "estado",
    "status_code": 200,
    "message": "Descripción del estado.",
    "data": {}
}
```

El código HTTP retornado por el servidor y el campo `status_code` representan el resultado protocolar de la solicitud. El campo `data` contiene los datos de la operación o `null` cuando la respuesta no los proporciona.

## Perfil

El perfil se obtiene mediante una ruta localizada:

```HTTP
GET /api/v1/{lang}/profile/
```

La ruta acepta los idiomas configurados por la aplicación y normaliza la etiqueta recibida antes de buscar el perfil correspondiente.

Actualmente están disponibles las siguientes variantes:

```text
es-co
pt-br
en-us
ja-jp
```

Cada perfil contiene su identificador, idioma, nombre, descripción y texto de presentación. La respuesta también incorpora los datos de contacto asociados al perfil.

La fuente de datos es un archivo JSON local y multilingüe. Su estructura completa es validada mediante Pydantic antes de formar la respuesta. Los caracteres Unicode son retornados directamente en el JSON, sin transformar los textos localizados en secuencias escapadas.

El endpoint utiliza un archivo de configuración JSON que permanece fuera del repositorio y de la imagen Docker. En producción, este archivo es incorporado en `/app/config/profile-config.json` durante la ejecución del contenedor. El archivo contiene un perfil para cada idioma admitido, además de los datos de contacto. Su estructura es la siguiente:

```JSON
{
    "perfiles": [
        {
            "id": 0,
            "idioma": "string",
            "nombre": "string",
            "descripcion": "string",
            "acerca_de": "string"
        }
    ],
    "contactos": {
        "linkedin": "string",
        "github": "string",
        "sitio_web": null,
        "correos_electronicos": [
            {
                "tipo": "string",
                "direccion": "string"
            }
        ],
        "telefonos": [
            {
                "tipo": "string",
                "formato": "string",
                "numero": "string"
            }
        ]
    }
}
```

Por lo que cada idioma va dentro de `perfiles` y es etiquetado en `idioma` por su sigla en formato `BCP 47` de globalización de nombres de idiomas. Una llamada de idioma no admitida en la URL produce una respuesta `404 Not Found`, pues se identifican en la aplicación como parte de la ruta. Los problemas relacionados con su existencia, lectura o validación en el archivo de configuración producen una respuesta `500 Internal Server Error`.

## OpenAPI

La especificación OpenAPI es generada a partir de la propia aplicación y de los contratos registrados en sus rutas.

Actualmente se utiliza OpenAPI 3.1.0. La especificación puede ser consultada directamente mediante:

```Shell
/api/v1/openapi.json
```

La documentación utilizada por Swagger UI también está disponible mediante:

```Shell
/api/v1/docs/openapi.json
```

Los `paths` son generados a partir de las rutas registradas por la aplicación, evitando mantener manualmente una segunda definición de las operaciones HTTP. Los schemas de las respuestas son generados a partir de los modelos Pydantic utilizados por la aplicación.

Conceptualmente:

```text
Rutas de la aplicación
=> paths

Contratos de datos
=> schemas

Paths + schemas
=> especificación OpenAPI
```

La especificación también incluye los modelos asociados a la validación de las solicitudes, como las respuestas HTTP `422 Unprocessable Content`.

## Swagger UI

La documentación interactiva está disponible mediante Swagger UI.

```Shell
/api/v1/docs/swagger
```

Swagger UI consume la especificación OpenAPI generada por la aplicación y permite consultar las operaciones disponibles, sus contratos, respuestas esperadas y ejecutar solicitudes directamente desde la interfaz.

La validación remota de Swagger UI está deshabilitada mediante la configuración de `validatorUrl`, evitando depender de un servicio externo para validar una API ejecutada en un entorno local o privado.

## Pydantic

Los datos de la aplicación son definidos mediante contratos que establecen los campos, tipos y restricciones permitidos.

Los modelos comunes heredan de una clase base propia que configura el comportamiento general de validación. Los contratos rechazan propiedades adicionales no definidas explícitamente y las respuestas no permiten cambios después de ser creadas.

Conceptualmente:

```text
ApiModel
  |
  +-- StatusResponse
  |       |
  |       +-- OkResponse
  |       |       |
  |       |       +-- ProfileResponse
  |       |
  |       +-- NotFoundResponse
  |       +-- InternalServerErrorResponse
  |
  +-- ProfilePath
  +-- ProfileConfig
  +-- ProfileData
```

`StatusResponse` define la estructura común de las respuestas de estado. Los modelos derivados restringen los valores permitidos para cada respuesta concreta.

`ProfileConfig` valida la fuente completa del perfil y sus estructuras anidadas. `ProfileData` define los datos retornados y `ProfileResponse` integra estos datos en el contrato común de respuesta satisfactoria.

Las respuestas de las rutas son validadas mediante Pydantic antes de ser retornadas por la API.

## Fuentes de datos

La distribución de responsabilidades definida para el contenido es:

```text
Perfil
=> JSON local multilingüe

Proyectos
=> JSON local multilingüe
=> GitHub REST API

Blog
=> Markdown multilingüe
```

El perfil constituye la primera fuente implementada. Los recursos relacionados con proyectos y blog forman parte de las siguientes fases del desarrollo.

El frontend no deberá depender directamente de las fuentes de datos. `Sitio-api` será responsable de obtener, validar y normalizar la información antes de retornarla en JSON.

Esto permite que el frontend utilice una estructura estable independientemente de si determinada información proviene de GitHub, de un archivo local o de Markdown.

## Internacionalización

El sistema trabaja con etiquetas de idioma explícitas. Estas etiquetas no son inferidas automáticamente a partir del contenido.

Los textos localizables se mantienen separados de los datos que no dependen del idioma. La API conserva una misma estructura de respuesta para todas las variantes; el idioma solicitado modifica el contenido textual, no el contrato general del recurso.

La normalización de la etiqueta recibida permite procesar diferencias de mayúsculas y minúsculas sin modificar los identificadores almacenados en la fuente de datos.

## CORS

El acceso entre el frontend y la API se controla mediante CORS.

La configuración se aplica exclusivamente a las rutas bajo `/api/`. El origen permitido se obtiene desde el entorno de ejecución, evitando mantener un dominio específico escrito en el código.

Las solicitudes procedentes del origen configurado reciben la cabecera CORS correspondiente. Los orígenes desconocidos no reciben la cabecera `Access-Control-Allow-Origin` y la redirección ubicada fuera de `/api/` tampoco recibe cabeceras CORS.

## Configuración

La aplicación requiere dos variables de entorno:

```text
PROFILE_CONFIG_FILE
=> camino del archivo JSON utilizado por el endpoint de perfil

CORS_ALLOWED_ORIGIN
=> origen autorizado para realizar solicitudes desde el frontend
```

En producción, `PROFILE_CONFIG_FILE` apunta a `/app/config/profile-config.json`.  

Las variables de entorno deben estar disponibles al iniciar la aplicación. Sus valores proceden del sistema local o de la plataforma de ejecución y no se mantienen escritos directamente en el código.

## Docker

El `Dockerfile` construye el entorno de ejecución a partir de una imagen de Python, actualiza sus paquetes de sistema e instala las herramientas necesarias para obtener el código fuente.

La rama utilizada durante la construcción se controla mediante el argumento `SITIO_API_BRANCH`, cuyo valor predeterminado es `main`. Después de obtener el código, Docker instala el grupo de dependencias de producción declarado en `pyproject.toml` y verifica la consistencia de la instalación.

La imagen crea el directorio `/app/config`, pero no incorpora el archivo privado `profile-config.json`. Durante la ejecución, el entorno responsable del contenedor debe montar físicamente el archivo en `/app/config/profile-config.json`.

En el desarrollo local, el archivo se monta desde el equipo anfitrión. En producción, Northflank lo almacena como archivo secreto y lo inyecta en la misma ruta.

La aplicación es servida por Gunicorn en el puerto `5000`. El contenedor incluye una comprobación periódica de salud contra el endpoint `/api/v1/health/`.

`.dockerignore` excluye del contexto los entornos virtuales, caches, resultados de cobertura, pruebas, documentación, scripts auxiliares y demás archivos que no forman parte de la ejecución de producción.

La imagen se almacena de forma privada en GitHub Container Registry.

## Despliegue

La imagen de la aplicación es almacenada de forma privada en `GitHub Container Registry` y ejecutada mediante `Northflank Developer Sandbox` en la región `US - Central`.

Northflank utiliza las credenciales configuradas para obtener la imagen privada desde GitHub Container Registry. La plataforma proporciona las variables de entorno, monta el archivo privado de configuración del perfil, expone el puerto de la aplicación y supervisa el estado del contenedor.

```text
main
  |
  V
Construcción de la imagen
  |
  V
GitHub Container Registry
  |
  V
Northflank Developer Sandbox
  |
  +-- PROFILE_CONFIG_FILE
  +-- CORS_ALLOWED_ORIGIN
  +-- profile-config.json
  |
  V
sitio-api
```

El despliegue es validado mediante el endpoint de salud.

La construcción y publicación de nuevas imágenes todavía constituyen un proceso separado del workflow de integración y promoción. La configuración privada del perfil queda desacoplada de este proceso porque es administrada directamente por Northflank.

## Integración y promoción

La rama `dev` constituye la rama de integración del proyecto. Cada actualización ejecuta el workflow de validación, que comprueba padronización de código, los imports, las pruebas y la cobertura.

La promoción solo ocurre cuando todas las validaciones terminan correctamente. Una GitHub App dedicada realiza el cambio sobre la rama protegida `main`.

```text
dev
  |
  V
Ruff + isort + pytest + cobertura
  |
  V
GitHub App de promoción
  |
  V
main
```

El token normal de GitHub Actions dispone únicamente de permiso de lectura. La identidad autorizada para actualizar `main` es la GitHub App utilizada por el workflow de promoción.

## Validación

Los datos procesados por la aplicación son validados antes de ser utilizados o expuestos por la API.

Pydantic constituye el sistema principal para definir contratos, verificar tipos, controlar campos obligatorios y limitar estructuras permitidas.

La especificación OpenAPI dispone de pruebas que verifican sus rutas, respuestas y relaciones entre schemas. La configuración del perfil, las respuestas HTTP, CORS y las fuentes locales también son validados mediante pruebas dedicadas.

## Pruebas

Las pruebas automatizadas cubren la creación de la aplicación, las rutas, los manejadores de errores, los contratos Pydantic, la lectura de archivos, CORS y la documentación OpenAPI.

La suite se ejecuta en modo estricto, mide instrucciones y ramas, evita publicar un resultado de cobertura cuando existen pruebas fallidas y exige cobertura completa.

```Shell
python -m pytest -x -s -vv --strict --cov=. --cov-branch --no-cov-on-fail --cov-report=term-missing --cov-report=html --cov-fail-under=100
```

El resultado esperado es:

```text
Todas las pruebas aprobadas
100% de cobertura de instrucciones
100% de cobertura de ramas
```

## Licencia

Este proyecto está licenciado bajo GNU General Public License v3.0.
