# Generador de Documentos Formateados desde Markdown

Este script transforma un archivo Markdown de entrada en un documento con formato legal o profesional, listo para uso institucional.

Archivo del script: `generate_formatted_doc.py`

## Requisitos

- Python 3.9 o superior.
- Archivo de entrada en formato Markdown (`.md`).

## Uso rapido

Desde la carpeta del proyecto:

```bash
python generate_formatted_doc.py --input markdown/marco_legal_y_etico.md --output output/marco_legal_formateado.md --profile marco_legal --style legal --entity "Tu Institucion" --country "Costa Rica" --contact "legal@tuorg.org"
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
