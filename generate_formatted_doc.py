#!/usr/bin/env python3
"""
Generate a formatted legal/professional markdown document from a README.md file.

Usage examples:
    python generate_formatted_doc.py --input markdown/README.md --output output/marco_legal_formateado.md --profile marco_legal
    python generate_formatted_doc.py --input markdown/README.md --entity "Fundacion X" --country "Costa Rica"
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import List, Tuple


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_lines(text: str) -> List[str]:
    # Normalize Windows/Mac line endings and trim trailing spaces
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return [line.rstrip() for line in lines]


def parse_sections(lines: List[str]) -> List[Tuple[int, str, List[str]]]:
    """
    Parse markdown headings and return sections as tuples:
      (heading_level, heading_text, content_lines)
    """
    sections: List[Tuple[int, str, List[str]]] = []
    current_level = 1
    current_title = "Contenido inicial"
    current_content: List[str] = []

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            # flush current section
            if current_content or sections:
                sections.append((current_level, current_title, current_content))
            current_level = len(match.group(1))
            current_title = match.group(2).strip()
            current_content = []
        else:
            current_content.append(line)

    sections.append((current_level, current_title, current_content))
    # Remove empty sections created by leading heading if needed
    cleaned = []
    for level, title, content in sections:
        if title == "Contenido inicial" and not "\n".join(content).strip():
            continue
        cleaned.append((level, title, content))
    return cleaned


def sanitize_heading(text: str) -> str:
    text = re.sub(r"`", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or "Seccion"


def compact_content(content_lines: List[str]) -> List[str]:
    """Collapse excessive empty lines while preserving markdown lists."""
    out: List[str] = []
    empty_streak = 0
    for line in content_lines:
        if not line.strip():
            empty_streak += 1
            if empty_streak <= 1:
                out.append("")
            continue
        empty_streak = 0
        out.append(line)
    # trim edge empties
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def render_header(entity: str, country: str, contact: str, profile: str) -> List[str]:
    today = dt.date.today().isoformat()

    if profile == "marco_legal":
        title = "# POLITICA DE TRATAMIENTO DE DATOS, USO ACEPTABLE Y GOBERNANZA ETICA"
        subtitle = "# Plataforma de Inteligencia Preventiva"
    else:
        title = "# DOCUMENTO INSTITUCIONAL"
        subtitle = "# Version formateada desde README"

    return [
        title,
        subtitle,
        "",
        "Version: 1.0",
        f"Fecha de emision: {today}",
        f"Titular/Responsable: {entity}",
        f"Pais/Jurisdiccion: {country}",
        f"Contacto: {contact}",
        "",
        "Vigencia: A partir de [COMPLETAR]",
        "Ultima revision: [COMPLETAR]",
        "",
        "Aprobaciones (firmas internas):",
        "- Representante legal / Direccion: [NOMBRE - CARGO - FECHA]",
        "- Oficial de seguridad / TI: [NOMBRE - CARGO - FECHA]",
        "- Enlace institucional: [NOMBRE - CARGO - FECHA]",
        "",
        "---",
        "",
    ]


def render_legal_sections(sections: List[Tuple[int, str, List[str]]]) -> List[str]:
    """
    Render sections into legal-style clauses:
    - H1/H2 become major sections
    - H3+ become subclauses under current section
    """
    output: List[str] = []
    major_count = 0
    clause_count = 0

    for level, title, content in sections:
        title = sanitize_heading(title)
        body = compact_content(content)

        # Treat level <=2 as major section
        if level <= 2:
            major_count += 1
            clause_count = 0
            output.append(f"## {to_roman(major_count)}. {title.upper()}")
            output.append("")
            if body:
                clause_count += 1
                output.append(f"### Clausula {major_count}.{clause_count}. Disposicion general")
                output.append(render_clause_body(body))
                output.append("")
            continue

        # level >=3 -> clause inside current major section
        if major_count == 0:
            major_count = 1
            output.append("## I. DISPOSICIONES")
            output.append("")

        clause_count += 1
        output.append(f"### Clausula {major_count}.{clause_count}. {title}")
        output.append(render_clause_body(body))
        output.append("")

    return output


def render_professional_sections(sections: List[Tuple[int, str, List[str]]]) -> List[str]:
    output: List[str] = []
    for level, title, content in sections:
        title = sanitize_heading(title)
        body = compact_content(content)
        heading_level = max(2, min(4, level))
        output.append("#" * heading_level + f" {title}")
        output.append("")
        if body:
            output.extend(body)
            output.append("")
    return output


def render_clause_body(lines: List[str]) -> str:
    if not lines:
        return "Sin contenido declarado."
    return "\n".join(lines)


def to_roman(number: int) -> str:
    numerals = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    result = []
    n = number
    for value, symbol in numerals:
        while n >= value:
            result.append(symbol)
            n -= value
    return "".join(result)


def render_annexes(profile: str) -> List[str]:
    annexes = ["---", "", "## ANEXOS", ""]

    annexes.extend(
        [
            "Anexo A. Matriz de roles y permisos (plantilla)",
            "- Reportante: crear reporte; sin lectura.",
            "- Analista institucional: leer resultados agregados; validar alertas.",
            "- Administrador tecnico: operacion de infraestructura con minimo privilegio.",
            "",
            "Anexo B. Registro de revision legal/etica (plantilla)",
            "- Fecha de revision: [COMPLETAR]",
            "- Revisor externo: [NOMBRE - ORGANIZACION]",
            "- Observacion: [DESCRIPCION]",
            "- Severidad: [BAJA/MEDIA/ALTA]",
            "- Accion correctiva: [DESCRIPCION]",
            "- Estado: [PENDIENTE/EN CURSO/RESUELTO]",
            "",
        ]
    )

    if profile == "marco_legal":
        annexes.extend(
            [
                "Anexo C. Texto breve para presentacion",
                '"La plataforma opera bajo minimizacion de datos, no identifica personas y requiere validacion humana para escalar alertas. Sus salidas son de apoyo preventivo y no sustituyen procesos judiciales."',
                "",
            ]
        )

    return annexes


def build_document(
    readme_text: str,
    entity: str,
    country: str,
    contact: str,
    style: str,
    profile: str,
) -> str:
    lines = normalize_lines(readme_text)
    sections = parse_sections(lines)

    output: List[str] = []
    output.extend(render_header(entity, country, contact, profile))

    if style == "legal":
        output.extend(render_legal_sections(sections))
    else:
        output.extend(render_professional_sections(sections))

    output.extend(render_annexes(profile))

    # Normalize final newlines
    doc = "\n".join(output).rstrip() + "\n"
    return doc


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate formatted legal/professional markdown from README.md"
    )
    parser.add_argument(
        "--input",
        "-i",
        default="markdown/README.md",
        help="Input markdown path",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output/marco_legal_formateado.md",
        help="Output markdown path",
    )
    parser.add_argument(
        "--style",
        choices=["legal", "professional"],
        default="legal",
        help="Output style",
    )
    parser.add_argument(
        "--profile",
        choices=["marco_legal", "generic"],
        default="marco_legal",
        help="Formatting profile",
    )
    parser.add_argument(
        "--entity",
        default="[NOMBRE DE LA ENTIDAD RESPONSABLE]",
        help="Entity/owner name",
    )
    parser.add_argument("--country", default="Costa Rica", help="Country/jurisdiction")
    parser.add_argument(
        "--contact",
        default="[CORREO/TELEFONO/DOMICILIO]",
        help="Contact line",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    readme_text = read_text(input_path)
    formatted = build_document(
        readme_text=readme_text,
        entity=args.entity,
        country=args.country,
        contact=args.contact,
        style=args.style,
        profile=args.profile,
    )

    output_path.write_text(formatted, encoding="utf-8")
    print(f"OK: Generated {output_path}")


if __name__ == "__main__":
    main()
