# SANCA · Gestor de Estudiantes y Cursos

> Aplicación de escritorio para la gestión de datos de estudiantes y cursos del **Centro de Formación Profesional N.° 401 — Escuela de Oficios SANCA**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational.svg)](https://docs.python.org/3/library/tkinter.html)
[![SQLite](https://img.shields.io/badge/DB-SQLite-003B57.svg)](https://www.sqlite.org/)
[![Licencia](https://img.shields.io/badge/licencia-MIT-green.svg)](LICENSE)

## 📋 Tabla de contenidos

- [Descripción](#-descripción)
- [Capturas](#-capturas)
- [Características](#-características)
- [Stack tecnológico](#-stack-tecnológico)
- [Requisitos previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Base de datos](#-base-de-datos)
- [Roadmap](#-roadmap)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Autor](#-autor)

## 📖 Descripción

**SANCA** es una aplicación de escritorio desarrollada en Python para centralizar la administración de la información académica de la **Escuela de Oficios SANCA (CFP N.° 401)**.

Permite dar de alta estudiantes, organizar cursos y adjuntar documentación respaldatoria (PDF y DOCX) asociada a cada legajo, todo desde una interfaz gráfica simple y sin necesidad de conexión a internet. Los datos se guardan localmente en una base de datos SQLite, lo que facilita el respaldo y la portabilidad del sistema entre las computadoras del establecimiento.

El proyecto nació con el objetivo de reemplazar planillas sueltas y carpetas físicas por un registro único, ordenado y fácil de consultar por parte del personal administrativo.

## 📸 Capturas

<!-- Reemplazá estas rutas por capturas reales dentro de la carpeta docs/ -->

| Pantalla principal | Alta de estudiante |
|--------------------|--------------------|
| ![Pantalla principal](docs/captura-principal.png) | ![Alta estudiante](docs/captura-alta.png) |

## ✨ Características

- 🗂️ **Gestión de estudiantes:** alta, baja, modificación y consulta de legajos.
- 📚 **Gestión de cursos:** creación y administración de cursos y talleres de oficios.
- 📄 **Importación de documentos:** lectura y asociación de archivos **PDF** y **DOCX** a cada estudiante.
- 🖼️ **Soporte de imágenes:** visualización de fotos de legajo con Pillow.
- 🔎 **Búsqueda y filtrado** de registros desde la interfaz.
- 💾 **Persistencia local** con SQLite, sin dependencia de servidores externos.
- 🏫 **Branding institucional** embebido (logo SANCA en base64, no requiere archivos externos).
- 🧾 **Exportación / copia de respaldo** de la base de datos (función `shutil`).

## 🛠 Stack tecnológico

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3.10+ |
| Interfaz gráfica | Tkinter |
| Base de datos | SQLite 3 |
| Lectura de PDF | PyPDF2 |
| Lectura de DOCX | `zipfile` (XML interno) |
| Imágenes | Pillow (PIL) |
| Utilidades | `base64`, `re`, `textwrap`, `shutil`, `os` |

## 📦 Requisitos previos

- Python **3.10** o superior.
- `pip` actualizado.
- Sistema operativo: Windows, Linux o macOS (Tkinter viene incluido con Python; en Linux puede requerir `python3-tk`).

En Debian/Ubuntu:

```bash
sudo apt install python3-tk
