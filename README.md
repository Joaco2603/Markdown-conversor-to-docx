# Generador de Documentos Formateados desde Markdown

Este script transforma un archivo Markdown de entrada en un documento con formato legal o profesional, listo para uso institucional.

Archivo del script: `generate_formatted_doc.py`

## Requisitos

- Python 3.9 o superior.
- Archivo de entrada en formato Markdown (`.md`).

## Configuracion por entorno (.env)

Este proyecto soporta rutas y metadatos por variables de entorno para que funcione igual en cualquier equipo.

1. Copia la plantilla:

```bash
copy .env.example .env
```

2. Edita `.env` con tus rutas y datos.

Variables disponibles:

- `MD_INPUT_PATH`
- `MD_OUTPUT_PATH`
- `MD_STYLE`
- `MD_PROFILE`
- `MD_ENTITY`
- `MD_COUNTRY`
- `MD_CONTACT`
- `DOCX_INPUT_PATH`
- `DOCX_OUTPUT_PATH`

Nota: los argumentos por CLI siempre tienen prioridad sobre `.env`.

## Uso rapido

Desde la carpeta del proyecto:

```bash
python generate_formatted_doc.py --input markdown/marco_legal_y_etico.md --output output/marco_legal_formateado.md --profile marco_legal --style legal --entity "Tu Institucion" --country "Costa Rica" --contact "legal@tuorg.org"
```

Usando solo `.env` (sin pasar rutas):

```bash
python generate_formatted_doc.py
python md_to_docx.py
```

## Parametros

- `--input`, `-i`: archivo Markdown de entrada. Por defecto: `markdown/README.md`.
- `--output`, `-o`: archivo Markdown de salida. Por defecto: `output/marco_legal_formateado.md`.
- `--style`: estilo de salida. Opciones: `legal`, `professional`. Por defecto: `legal`.
- `--profile`: perfil de formato. Opciones: `marco_legal`, `generic`. Por defecto: `marco_legal`.
- `--entity`: nombre de la entidad responsable.
- `--country`: pais/jurisdiccion.
- `--contact`: linea de contacto institucional.

## Ejemplos

### 1) Formato legal para marco legal

```bash
python generate_formatted_doc.py -i markdown/marco_legal_y_etico.md -o output/marco_legal_formateado.md --style legal --profile marco_legal --entity "Open Impact" --country "Costa Rica" --contact "compliance@openimpact.org"
```

### 2) Formato profesional generico

```bash
python generate_formatted_doc.py -i markdown/marco_legal_y_etico.md -o output/documento_profesional.md --style professional --profile generic --entity "Open Impact" --country "Costa Rica" --contact "info@openimpact.org"
```

## Conversor a DOCX

```bash
python md_to_docx.py --input markdown/marco_legal_formateado.md --output output/marco_legal_formateado.docx
```

## Salida esperada

El script genera un documento con:

- Encabezado institucional (version, fecha, vigencia, aprobaciones).
- Estructura por secciones o clausulas (segun estilo).
- Anexos operativos reutilizables (roles, revision legal/etica, texto de presentacion).

## Notas

- Si el archivo de entrada no existe, el script termina con error y mensaje descriptivo.
- El estilo `legal` convierte titulos a una estructura por clausulas.
- Puedes usar cualquier `.md` como entrada, no solo `README.md`.
