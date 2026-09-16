"""
matcher.py — Intelligent String Matching Engine
AI-Powered Resume & ATS Optimizer

For every required JD skill, compute token-based string similarity against
resume skills. Categorize results and calculate a comprehensive ATS score.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from thefuzz import fuzz
from taxonomy import SKILL_TAXONOMY


# ──────────────────────────────────────────────────────────────
# DATA STRUCTURES
# ──────────────────────────────────────────────────────────────

@dataclass
class SkillMatchResult:
    """Result of matching a single JD skill against the resume."""
    required_skill: str          # Canonical JD skill name
    status: str                  # "Exact Match" | "Fuzzy Match" | "Missing"
    matched_resume_term: str     # The resume term that matched (or "—")
    similarity_score: int        # 0–100 token_sort_ratio


@dataclass
class ATSReport:
    """Full ATS diagnostic report."""
    ats_score: float                                 # 0.0–100.0
    total_jd_skills: int
    exact_count: int
    fuzzy_count: int
    missing_count: int
    skill_results: list[SkillMatchResult] = field(default_factory=list)

    @property
    def matched_count(self) -> int:
        return self.exact_count + self.fuzzy_count

    @property
    def missing_skills(self) -> list[str]:
        return [r.required_skill for r in self.skill_results if r.status == "Missing"]

    @property
    def exact_skills(self) -> list[SkillMatchResult]:
        return [r for r in self.skill_results if r.status == "Exact Match"]

    @property
    def fuzzy_skills(self) -> list[SkillMatchResult]:
        return [r for r in self.skill_results if r.status == "Fuzzy Match"]


# ──────────────────────────────────────────────────────────────
# MATCHING ENGINE
# ──────────────────────────────────────────────────────────────

def _best_fuzzy_score(
    jd_skill: str,
    resume_skills: dict[str, str],
) -> tuple[int, str]:
    """
    Compute the best fuzzy similarity between a JD skill (plus its aliases)
    and all resume skills (plus their aliases).

    We compare:
      • jd_skill canonical name  vs.  each resume canonical name
      • jd_skill canonical name  vs.  each resume matched-text
      • jd_skill aliases         vs.  each resume canonical name
      • jd_skill aliases         vs.  each resume alias

    Returns
    -------
    tuple[int, str]
        (best_score, best_matching_resume_term)
    """
    jd_lower = jd_skill.lower()
    jd_aliases = [a.lower() for a in SKILL_TAXONOMY.get(jd_skill, {}).get("aliases", [])]
    jd_variants = [jd_lower] + jd_aliases

    best_score = 0
    best_term = "—"

    for resume_canonical, resume_matched_text in resume_skills.items():
        resume_lower = resume_canonical.lower()
        resume_aliases = [a.lower() for a in SKILL_TAXONOMY.get(resume_canonical, {}).get("aliases", [])]
        resume_variants = [resume_lower, resume_matched_text.lower()] + resume_aliases

        for jv in jd_variants:
            for rv in resume_variants:
                score = fuzz.token_sort_ratio(jv, rv)
                if score > best_score:
                    best_score = score
                    best_term = resume_canonical

    return best_score, best_term


def run_matching(
    jd_skills: list[str],
    resume_skills: dict[str, str],
    match_threshold: int = 80,
    partial_threshold: int = 60,
) -> ATSReport:
    """
    Run the full ATS matching pipeline.

    Parameters
    ----------
    jd_skills : list[str]
        Canonical skill names required by the Job Description.
    resume_skills : dict[str, str]
        Mapping of canonical skill name -> matched substring from resume.
    match_threshold : int
        Minimum similarity for an "Exact Match" (default 80).
    partial_threshold : int
        Minimum similarity for a "Fuzzy Match" (default 60).

    Returns
    -------
    ATSReport
        Complete diagnostic report with per-skill results and ATS score.
    """
    results: list[SkillMatchResult] = []
    exact_count = 0
    fuzzy_count = 0
    missing_count = 0

    for jd_skill in jd_skills:
        # Quick-check: exact canonical match present in resume?
        if jd_skill in resume_skills:
            results.append(SkillMatchResult(
                required_skill=jd_skill,
                status="Exact Match",
                matched_resume_term=jd_skill,
                similarity_score=100,
            ))
            exact_count += 1
            continue

        # Fuzzy comparison against all resume skills
        best_score, best_term = _best_fuzzy_score(jd_skill, resume_skills)

        if best_score >= match_threshold:
            results.append(SkillMatchResult(
                required_skill=jd_skill,
                status="Exact Match",
                matched_resume_term=best_term,
                similarity_score=best_score,
            ))
            exact_count += 1
        elif best_score >= partial_threshold:
            results.append(SkillMatchResult(
                required_skill=jd_skill,
                status="Fuzzy Match",
                matched_resume_term=best_term,
                similarity_score=best_score,
            ))
            fuzzy_count += 1
        else:
            results.append(SkillMatchResult(
                required_skill=jd_skill,
                status="Missing",
                matched_resume_term="—",
                similarity_score=best_score,
            ))
            missing_count += 1

    # Deterministic ATS Score formula
    total = len(jd_skills) if jd_skills else 1
    ats_score = ((exact_count + 0.5 * fuzzy_count) / total) * 100
    ats_score = round(min(ats_score, 100.0), 1)

    # Sort results: Exact first, then Fuzzy, then Missing (within each, by score desc)
    status_order = {"Exact Match": 0, "Fuzzy Match": 1, "Missing": 2}
    results.sort(key=lambda r: (status_order.get(r.status, 9), -r.similarity_score))

    return ATSReport(
        ats_score=ats_score,
        total_jd_skills=len(jd_skills),
        exact_count=exact_count,
        fuzzy_count=fuzzy_count,
        missing_count=missing_count,
        skill_results=results,
    )
