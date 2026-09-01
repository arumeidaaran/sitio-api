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
      | HTTP
      V
sitio-api
Flask
      |
      V
Contenido, servicios y fuentes de datos
```

Durante el desarrollo local, la API será ejecutada mediante Docker y expuesta a través de la dirección IP del equipo anfitrión.

```text
IP del equipo
      |
      V
Docker
      |
      V
Flask
```

El contenedor utilizado durante el desarrollo deberá poder ser reutilizado posteriormente en la plataforma elegida para alojar el backend.

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

## Tecnologías

El backend utiliza Python y Flask.

Las dependencias de producción incluyen framework de API, WSGI, formateador de documentación, validador de tipos y retornos, y documentación técnica con soporte para Swagger UI.

Swagger UI proporciona una interfaz interactiva para consultar y ejecutar las operaciones documentadas por la API.

Las herramientas utilizadas durante el desarrollo incluyen validador de convenciones de Python, framework de pruebas unitarias y de cobertura de código.

Las dependencias son declaradas mediante `pyproject.toml`. Los archivos `requirements.txt` y `requirements_dev.txt` son mantenidos adicionalmente por motivos de compatibilidad con herramientas y automatizaciones existentes.

## API

La API es versionada desde su primera versión.

Actualmente utiliza OpenAPI 3.1.0 para describir formalmente sus operaciones, respuestas y schemas.

```text
sitio-api/
│
├── app.py
│
├── api/
│   └── v1/
│       ├── errors/
│       │   └── handlers.py
│       │
│       └── routes/
│           ├── root.py
│           └── health.py
│
├── services/
│   └── content.py
│
├── schemas/
│   ├── base.py
│   ├── responses.py
│   └── content.py
│
├── content/
│   ├── profile/
│   ├── projects/
│   └── blog/
│
├── tests/
│   ├── conftest.py
│   ├── test_app.py
│   └── api/
│       └── v1/
│           ├── errors/
│           │   └── test_handlers.py
│           │
│           └── routes/
│               ├── test_root.py
│               └── test_health.py
│
├── pyproject.toml
├── Dockerfile
├── .dockerignore
└── .gitignore
```

`app.py` constituye el punto de entrada de la aplicación.

La aplicación genera una especificación OpenAPI a partir de sus rutas y contratos de datos.

También es responsable de registrar los manejadores de errores y la redirección de la raíz de la aplicación hacia la versión actual de la API.

Actualmente están disponibles:

```text
/
=> redirección hacia /api/v1/

/api/v1/
=> raíz de la versión actual

/api/v1/health
=> comprobación de estado de la API

/api/v1/openapi.json
=> especificación OpenAPI de la API

/api/v1/docs/
=> documentación de la API

/api/v1/docs/swagger
=> interfaz Swagger UI

/api/v1/docs/openapi.json
=> especificación utilizada por la documentación
```

La versión `v1` mantiene separadas sus rutas y sus manejadores de errores.

Las rutas registradas por la aplicación son incorporadas automáticamente a la especificación OpenAPI.

Las rutas documentan sus posibles respuestas mediante modelos Pydantic.

Actualmente se utilizan contratos específicos para respuestas satisfactorias y errores HTTP.

```text
OkResponse
=> respuesta satisfactoria

NotFoundResponse
=> recurso no encontrado

InternalServerErrorResponse
=> error interno del servidor
```

Los errores HTTP `404 Not Found` y `500 Internal Server Error` disponen de respuestas JSON propias y son registrados globalmente por la aplicación.

Las respuestas siguen una estructura común:

```json
{
    "status": "estado",
    "message": "Descripción del estado."
}
```

Los códigos HTTP continúan siendo responsables de representar el resultado protocolar de cada solicitud.

Las rutas y contratos adicionales serán incorporados progresivamente durante el desarrollo.

## OpenAPI

La especificación OpenAPI es generada a partir de la propia aplicación y de los contratos registrados en sus rutas.

Actualmente se utiliza OpenAPI 3.1.0.

La especificación puede ser consultada directamente mediante:

```text
/api/v1/openapi.json
```

La documentación utilizada por Swagger UI también está disponible mediante:

```text
/api/v1/docs/openapi.json
```

Los `paths` son generados a partir de las rutas registradas por la aplicación, evitando mantener manualmente una segunda definición de las operaciones HTTP.

Los schemas de las respuestas son generados a partir de los modelos Pydantic utilizados por la aplicación.

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

```text
/api/v1/docs/swagger
```

Swagger UI consume la especificación OpenAPI generada por la aplicación y permite consultar las operaciones disponibles, sus contratos, respuestas esperadas y ejecutar solicitudes directamente desde la interfaz.

La validación remota de Swagger UI está deshabilitada mediante la configuración de `validatorUrl`, evitando depender de un servicio externo para validar una API ejecutada en un entorno local o privado.

La validación del contrato puede realizarse localmente mediante las herramientas utilizadas por el propio proyecto.

## Pydantic

Los datos de la aplicación son definidos mediante contratos que establecen los campos, tipos y restricciones permitidos.

Los modelos comunes heredan de una clase base propia que configura el comportamiento general de validación.

Los contratos internos rechazan propiedades adicionales no definidas explícitamente.

Conceptualmente:

```text
ApiModel
  |
  +-- StatusResponse
          |
          +-- OkResponse
          +-- NotFoundResponse
          +-- InternalServerErrorResponse
```

`StatusResponse` define la estructura común de las respuestas de estado.

Los modelos derivados restringen los valores permitidos para cada respuesta concreta.

Las respuestas de las rutas son validadas mediante Pydantic antes de ser retornadas por la API.

Los futuros contratos relacionados con perfil, proyectos, blog, configuración y fuentes externas también utilizarán Pydantic para validar sus estructuras.

## Estructura del contenido

El sitio será organizado inicialmente alrededor de tres áreas principales:

```text
Perfil
Proyectos
Blog
```

Estas áreas utilizarán una misma API, pero no necesariamente la misma fuente de datos.

### Perfil

La información del perfil será mantenida localmente en un archivo de configuración estructurado en JSON.

El contenido será almacenado por idioma y podrá incluir información como la presentación personal, trayectoria profesional, formación, tecnologías, áreas de actuación e idiomas.

Los datos serán validados mediante modelos Pydantic antes de ser utilizados o expuestos por la API.

### Proyectos

Los proyectos combinarán dos fuentes de información.

Un archivo JSON local será responsable de definir qué repositorios forman parte del sitio, proporcionar un identificador numérico estable para cada proyecto y almacenar los textos dependientes del idioma, principalmente las descripciones.

La API de GitHub será utilizada para recuperar información técnica y objetiva de los repositorios, como nombre, enlace, lenguajes, distribución de lenguajes, fechas, licencia, tópicos, estrellas, forks y otros metadatos que puedan ser útiles para el frontend.

Conceptualmente:

```text
Configuración JSON
        |
        | Identificador y contenido localizado
        |
        +----------+
                   |
                   V
            API del proyecto
                   ^
                   |
        +----------+
        |
GitHub REST API
        |
        | Información técnica
```

Los identificadores internos de los proyectos serán numéricos y permanecerán independientes del nombre del repositorio.

Ejemplo conceptual:

```json
{
    "id": 1,
    "repository": "usuario_de_github/nome-del-proyecto",
    "descriptions": {
        "es-CO": "Descripción del proyecto.",
        "pt-BR": "Descrição do projeto.",
        "en-US": "Project description.",
        "ja-JP": "プロジェクトの説明。"
    }
}
```

El nombre del repositorio no será utilizado como identificador interno.

Tanto la configuración local como los datos obtenidos desde GitHub serán normalizados y validados antes de formar parte de una respuesta de la API.

### Blog

El blog utilizará archivos Markdown como fuente principal de contenido.

Cada publicación podrá disponer de versiones independientes para los idiomas soportados. Los metadatos asociados permitirán identificar la publicación, el idioma y demás propiedades necesarias para procesarla y exponerla mediante la API.

Markdown será utilizado para el contenido editorial del blog y no como formato general de configuración de la aplicación.

Los metadatos asociados a las publicaciones serán validados mediante modelos Pydantic.

## Fuentes de datos

La distribución inicial de responsabilidades será:

```text
Perfil
=> JSON local multilingüe

Proyectos
=> JSON local multilingüe
=> GitHub REST API

Blog
=> Markdown multilingüe
```

El frontend no deberá depender de estas fuentes directamente. `Sitio-api` será responsable de obtener, validar y normalizar los datos antes de retornarlos en JSON.

Esto permite que el frontend utilice una estructura estable independientemente de si determinada información proviene de GitHub, de un archivo local o de Markdown.

## Internacionalización

El sistema será preparado para trabajar con múltiples idiomas.

Los textos localizables serán mantenidos separadamente de los datos técnicos que no dependen del idioma.

Por ejemplo, un proyecto tendrá un único identificador, repositorio, enlace y conjunto de datos técnicos, mientras que su descripción podrá disponer de una versión para cada idioma soportado.

La API deberá mantener una misma estructura de respuesta para todos los idiomas. El idioma solicitado modificará el contenido textual, no el contrato general del recurso.

Las etiquetas de idioma serán explícitas y no serán inferidas automáticamente a partir del contenido.

Inicialmente se prevé soporte para variantes como:

```text
es-CO
pt-BR
en-US
ja-JP
```

## Validación

Los datos procesados por la aplicación serán validados antes de ser utilizados o expuestos por la API.

Pydantic constituye el sistema principal para definir contratos de datos, verificar tipos, controlar campos obligatorios y limitar estructuras permitidas.

Las respuestas de los endpoints actuales son validadas.

Los datos provenientes de archivos locales, Markdown, servicios internos y fuentes externas utilizarán modelos específicos de acuerdo con el origen y el contrato esperado.

Los identificadores de entidades como proyectos serán representados mediante valores enteros.

La especificación de la API forma parte de su infraestructura y debe poder ser validada de forma independiente.

## Pruebas

Las pruebas automatizadas utilizan un framework de pruebas unitarias y herramientas de cobertura de código.

Las respuestas de error son probadas tanto directamente mediante sus manejadores como mediante solicitudes HTTP realizadas contra la aplicación.

La especificación de la API también dispone de una prueba dedicada para verificar que pueda ser obtenida y contenga los elementos principales esperados.

La cobertura puede ser consultada desde la consola y generada también en formato HTML mediante este comando:

```Shell
pytest -x --cov=. --cov-report=term-missing --cov-report=html
```

La suite debe tener la cobertura completa:
- Todas las pruebas aprobadas
- 100% de cobertura


## Licencia

Este proyecto está licenciado bajo GNU General Public License v3.0.