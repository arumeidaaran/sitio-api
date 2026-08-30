# sitio-api

API del sitio personal, desarrollada con Flask y orientada a contenido, internacionalización y servicios para el frontend.

## Objetivo

`site-api` constituye la capa de backend del sitio personal.

Su función es procesar y exponer contenido para el frontend, manteniendo separadas la lógica de la aplicación y la capa de presentación.

El contenido textual será mantenido principalmente mediante archivos Markdown, acompañados de metadatos que permitan identificar su función, idioma y relación con otras versiones del mismo contenido.

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
Contenido y lógica
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

## Tecnologías

El backend utiliza Python y Flask.

Docker será utilizado para proporcionar un entorno reproducible de ejecución y facilitar posteriormente el despliegue de la aplicación en una plataforma externa.

## API

La API será versionada desde su primera versión.

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
│   └── content.py
│
├── content/
│   ├── pages/
│   ├── projects/
│   └── blog/
│
tests/
├── conftest.py
├── test_app.py
├── api/
│   └── v1/
│       └── routes/
│           ├── test_root.py
│           └── test_health.py
│
├── pyproject.toml
├── Dockerfile
├── .dockerignore
└── .gitignore
```

`app.py` constituye el punto de entrada de la aplicación Flask y es responsable de registrar los blueprints, los manejadores de errores y la redirección de la raíz de la aplicación hacia la versión actual de la API.

La versión `v1` mantiene separadas sus rutas y sus tratativas de errores. Actualmente expone la raíz `/api/v1/` y el endpoint de salud `/api/v1/health`.

** Las rutas y contratos serán definidos progresivamente durante el desarrollo.

## Contenido

El contenido será almacenado principalmente en archivos Markdown.

Cada documento podrá contener un encabezado de metadatos destinado a identificar características como el tipo de contenido, su identificador interno y el idioma correspondiente.

Ejemplo:

```yaml
---
type: page
content_id: home
language: es
---
```

La estructura definitiva de estos metadatos será definida conforme se desarrollen los diferentes tipos de contenido.

## Internacionalización

El sistema será preparado para trabajar con múltiples idiomas.

Las diferentes versiones lingüísticas de un mismo contenido podrán ser relacionadas mediante identificadores comunes, permitiendo que el frontend determine las traducciones disponibles para cada recurso.

## Licencia

Este proyecto está licenciado bajo GNU General Public License v3.0.