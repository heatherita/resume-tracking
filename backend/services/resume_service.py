
from __future__ import annotations

import argparse
import shutil
import subprocess
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import psycopg2
import yaml
from config.settings import BASE_STORAGE_PATH

logger = logging.getLogger("jobtelem")

def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def norm_tags(tags: Any) -> set[str]:
    logger.debug(f"Normalizing tags: {tags}")
    if tags is None:
        return set()
    if isinstance(tags, str):
        return {tags.lower().strip()}
    if isinstance(tags, list):
        return {str(t).lower().strip() for t in tags}
    return {str(tags).lower().strip()}


def bullet_included(
    bullet_tags: set[str],
    include: set[str],
    exclude: set[str],
    mode: str,
) -> bool:
    # Exclude always wins
    logger.info(f"Checking bullet with tags {bullet_tags} against include={include}, exclude={exclude}, mode={mode}")
    if exclude and (bullet_tags & exclude):
        return False

    # If no include filter, keep everything (except excluded)
    if not include:
        return True

    if mode == "any":
        return bool(bullet_tags & include)
    if mode == "all":
        return include.issubset(bullet_tags)
    raise ValueError(f"Unknown mode: {mode}")


def md_escape(s: str) -> str:
    return s.replace("\r\n", "\n").strip()


def render_header(data: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# {md_escape(data.get('name',''))}".strip())
    lines.extend(["", "----", "\n"])

    contact_bits = []
    for k in ("location", "phone", "email"):
        v = data.get(k)
        if v:
            contact_bits.append(md_escape(str(v)))
    if contact_bits:
        lines.append(f"### {' • '.join(contact_bits)}")
    lines.append("")
    return "\n".join(lines)


def render_summary(data: dict[str, Any],
                   include: set[str],
                    exclude: set[str],
    mode: str,) -> str:
    out = []
    kept = []
    for b in data.get("summary") or []:
        text = md_escape(str(b.get("text", "")))
        tags = norm_tags(b.get("tags"))
        if text and bullet_included(tags, include, exclude, mode):
            kept.append(text)

    if kept:
        out = ["## Professional Summary", "", "----", "\n"]
        for t in kept:
            out.append("")
            out.append(md_escape(t))
        out.append("")
        return "\n".join(out)
    else:
        return ""

def render_certification(data: dict[str, Any],
                   include: set[str],
                    exclude: set[str],
    mode: str,) -> str:
    out = []
    kept = []
    for b in data.get("certification") or []:
        header = md_escape(str(b.get("header", "")))
        tags = norm_tags(b.get("tags"))
        if header and bullet_included(tags, include, exclude, mode):
            kept.append(f"**{header}**")

        text = md_escape(str(b.get("text", "")))
        tags = norm_tags(b.get("tags"))
        if text and bullet_included(tags, include, exclude, mode):
            kept.append(text)

    if kept:
        out.extend(["## Certification", "", "----", "\n"])
        for t in kept:
            out.append("")
            out.append(t)
        out.append("")
        return "\n".join(out)
    else:
        return ""


def render_skills(data: dict[str, Any],
                  include: set[str],
                  exclude: set[str],
                  mode: str,
                  ) -> str:
    skills = data.get("skills") or []
    if not skills:
        return ""
    out = ["## Technical Skills", "", "----", "\n"]
    kept = []

    for s in skills or []:
        header = md_escape(s.get("header"))
        text = md_escape(s.get("skill"))
        tags = norm_tags(s.get("tags"))
        if header and text and bullet_included(tags, include, exclude, mode):
            kept.append(f"- **{md_escape(str(header))}** {md_escape(str(text))}")

    if kept:
        for t in kept:
            out.append(f"{t}")
    out.append("")
    return "\n".join(out)


def render_experience(
    data: dict[str, Any],
    include: set[str],
    exclude: set[str],
    mode: str,
) -> str:
    exp = data.get("experience") or []
    if not exp:
        return ""
    out = ["## Professional Experience", "", "----", "\n"]
    for role in exp:
        company = md_escape(str(role.get("company","")))
        title = md_escape(str(role.get("title","")))
        location = md_escape(str(role.get("location","")))
        dates = md_escape(str(role.get("dates","")))
        heading_company = f"**{company} — {title}**".strip()
        heading_location =f"{location} ({dates})".strip()
        out.extend([heading_company, "", heading_location,""])

        kept = []
        for b in role.get("bullets") or []:
            text = md_escape(str(b.get("text","")))
            tags = norm_tags(b.get("tags"))
            if text and bullet_included(tags, include, exclude, mode):
                kept.append(text)

        if kept:
            for t in kept:
                out.append(f"- {t}")
        else:
            out.append("- (No bullets matched selected tags.)")

        out.append("")
    return "\n".join(out)


def render_projects(
    data: dict[str, Any],
    include: set[str],
    exclude: set[str],
    mode: str,
) -> str:
    projects = data.get("projects") or []
    if not projects:
        return ""
    out = ["## Projects", "", "----", "\n"]
    for p in projects:
        name = md_escape(str(p.get("name","")))
        dates = md_escape(str(p.get("dates","")))
        out.extend([f"**{name}** ({dates})".strip(),""])

        kept = []
        for b in p.get("bullets") or []:
            text = md_escape(str(b.get("text","")))
            tags = norm_tags(b.get("tags"))
            if text and bullet_included(tags, include, exclude, mode):
                kept.append(text)

        if kept:
            for t in kept:
                out.append(f"- {t}")
        else:
            out.append("- (No bullets matched selected tags.)")
        out.append("")
    return "\n".join(out)


def render_education(data: dict[str, Any]) -> str:
    edu = data.get("education") or []
    if not edu:
        return ""
    out = ["## Education", "", "----", "\n"]
    for e in edu:
        school = md_escape(str(e.get("school","")))
        detail = md_escape(str(e.get("detail","")))
        year = md_escape(str(e.get("year","")))
        bits = [b for b in [school, detail, year] if b]
        out.append("- " + ", ".join(bits))
    out.append("")
    return "\n".join(out)


def build_md(data: dict[str, Any], include: set[str], exclude: set[str], mode: str) -> str:
    logger.info(f"Building markdown with include={include}, exclude={exclude}, mode={mode}")
    parts = [
        render_header(data),
        render_summary(data, include, exclude, mode),
        render_certification(data, include, exclude, mode),
        render_skills(data, include, exclude, mode),
        render_experience(data, include, exclude, mode),
        render_projects(data, include, exclude, mode),
        render_education(data),
    ]
    return "\n".join([p for p in parts if p]).strip() + "\n"


def create_odt_from_md():
    md_path = Path(BASE_STORAGE_PATH) / "resume.md"
    odt_path = Path(BASE_STORAGE_PATH) / "resume.odt"
    
    ref_doc_path = Path(__file__).resolve().parents[1] / "config" / "custom-reference.odt"
    cmd = [
    "pandoc",
    str(md_path),
    "--reference-doc", str(ref_doc_path),
    "-t","odt",
    "-o", str(odt_path),
    ]    
    subprocess.run(cmd, check=True)
    return odt_path


def create_resume_pdf_from_md(pdf_engine: str = "tectonic"):
    md_path = Path(BASE_STORAGE_PATH) / "resume.md"
    pdf_path = Path(BASE_STORAGE_PATH) / "resume.pdf"
    template_path = Path(__file__).resolve().parents[1] / "config" / "resume_template.tex"
    cmd = [
        "pandoc",
        str(md_path),
        "--pdf-engine", pdf_engine,
        "--template", str(template_path),
        # "-V", "geometry:margin=0.75in",
        "-V", "fontsize=10pt",
        "-V", "mainfont=DejaVu Sans",
        "-V", "sansfont=DejaVu Sans",
        # "-V", "linestretch=1.05",
        "-o", str(pdf_path),
    ]
    subprocess.run(cmd, check=True)
    return pdf_path
            
    