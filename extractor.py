"""
extractor.py — Text Extraction & NLP Processing
AI-Powered Resume & ATS Optimizer

Handles PDF parsing (via pdfplumber), text cleaning, and skill
extraction using regex word-boundary matching against the curated taxonomy.
"""

import re
import io
from taxonomy import SKILL_TAXONOMY


# ──────────────────────────────────────────────────────────────
# PDF / TEXT EXTRACTION
# ──────────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from an uploaded PDF file using pdfplumber.

    Parameters
    ----------
    pdf_file : file-like object (e.g. Streamlit UploadedFile)
        The PDF file to parse.

    Returns
    -------
    str
        Concatenated text from all pages.
    """
    import pdfplumber

    text_parts: list[str] = []
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception as exc:
        raise RuntimeError(f"Failed to parse PDF: {exc}") from exc

    return "\n".join(text_parts)


# ──────────────────────────────────────────────────────────────
# TEXT CLEANING
# ──────────────────────────────────────────────────────────────

def clean_text(raw_text: str) -> str:
    """
    Normalize and clean raw text for skill extraction.

    Steps
    -----
    1. Convert to lowercase.
    2. Replace common ligatures and special characters.
    3. Collapse multiple whitespace into single spaces.
    4. Strip leading/trailing whitespace.
    """
    text = raw_text.lower()

    # Normalize common ligatures / unicode artifacts
    replacements = {
        "\u2019": "'",   # right single quote
        "\u2018": "'",   # left single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2022": " ",   # bullet
        "\u00b7": " ",   # middle dot
        "\uf0b7": " ",   # PDF bullet artifact
        "\n": " ",
        "\r": " ",
        "\t": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ──────────────────────────────────────────────────────────────
# RULE-BASED SKILL EXTRACTION
# ──────────────────────────────────────────────────────────────

# Pre-compiled patterns for skills that need special boundary handling.
# For most skills we use word-boundary regex; for very short or symbolic
# skill names (C, C++, C#, R) we build custom patterns.

_SPECIAL_PATTERNS: dict[str, re.Pattern] = {}


def _build_pattern(skill_name: str) -> re.Pattern:
    """
    Build a compiled regex pattern that matches a skill name
    (or any of its aliases) in cleaned text, using word boundaries
    to prevent substring collisions.

    Special handling for:
    - Very short names (C, R) — require non-alphanumeric boundaries.
    - Names with special chars (C++, C#) — escape properly.
    - "Java" must NOT match "javascript".
    """
    entry = SKILL_TAXONOMY[skill_name]
    variants = [skill_name.lower()] + [a.lower() for a in entry["aliases"]]

    sub_patterns: list[str] = []
    for variant in variants:
        escaped = re.escape(variant)

        # Special case: single-letter skill names (C, R)
        if len(variant) == 1:
            # Match the letter surrounded by non-word chars or start/end
            sub_patterns.append(rf"(?<![a-zA-Z]){escaped}(?![a-zA-Z#+])")
        elif variant in ("java",):
            # "java" must not match "javascript" / "javafx" is ok? Let's be strict.
            sub_patterns.append(rf"\b{escaped}\b(?!\s*script)")
        else:
            sub_patterns.append(rf"\b{escaped}\b")

    combined = "|".join(sub_patterns)
    return re.compile(combined, re.IGNORECASE)


def _get_pattern(skill_name: str) -> re.Pattern:
    """Retrieve (and cache) the regex pattern for a skill."""
    if skill_name not in _SPECIAL_PATTERNS:
        _SPECIAL_PATTERNS[skill_name] = _build_pattern(skill_name)
    return _SPECIAL_PATTERNS[skill_name]


def extract_skills_from_text(text: str) -> dict[str, str]:
    """
    Scan cleaned text against the full taxonomy using regex patterns.

    Returns
    -------
    dict[str, str]
        Mapping of canonical skill name -> matched substring found in text.
        Only skills with at least one regex hit are included.
    """
    cleaned = clean_text(text)
    found_skills: dict[str, str] = {}

    for skill_name in SKILL_TAXONOMY:
        pattern = _get_pattern(skill_name)
        match = pattern.search(cleaned)
        if match:
            found_skills[skill_name] = match.group(0).strip()

    return found_skills


def extract_skills_from_jd(jd_text: str) -> list[str]:
    """
    Extract canonical skill names mentioned in a job description.

    Parameters
    ----------
    jd_text : str
        Raw job description text.

    Returns
    -------
    list[str]
        Sorted list of canonical skill names found.
    """
    found = extract_skills_from_text(jd_text)
    return sorted(found.keys())
