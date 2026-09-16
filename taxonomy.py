"""
taxonomy.py — Curated Skill Lexicon
AI-Powered Resume & ATS Optimizer

Contains a structured dictionary of 80+ industry skills organized by category,
each with known aliases/variants to improve matching accuracy.
"""

# ──────────────────────────────────────────────────────────────
# SKILL TAXONOMY
# Each entry:  canonical_name -> { "category": str, "aliases": [str, ...] }
# Aliases are common alternate spellings, abbreviations, or brand names
# that should be treated as equivalent during matching.
# ──────────────────────────────────────────────────────────────

SKILL_TAXONOMY: dict[str, dict] = {

    # ── Programming Languages ────────────────────────────────
    "Python":        {"category": "Programming Languages", "aliases": ["python3", "python 3", "py"]},
    "Java":          {"category": "Programming Languages", "aliases": ["core java", "java se", "java ee"]},
    "C++":           {"category": "Programming Languages", "aliases": ["cpp", "c plus plus", "cplusplus"]},
    "C":             {"category": "Programming Languages", "aliases": ["c language", "c programming"]},
    "C#":            {"category": "Programming Languages", "aliases": ["csharp", "c sharp", "c-sharp"]},
    "JavaScript":    {"category": "Programming Languages", "aliases": ["js", "es6", "ecmascript", "es2015"]},
    "TypeScript":    {"category": "Programming Languages", "aliases": ["ts", "typescript"]},
    "Go":            {"category": "Programming Languages", "aliases": ["golang"]},
    "Rust":          {"category": "Programming Languages", "aliases": ["rustlang"]},
    "Ruby":          {"category": "Programming Languages", "aliases": ["ruby lang"]},
    "PHP":           {"category": "Programming Languages", "aliases": ["php7", "php8"]},
    "Swift":         {"category": "Programming Languages", "aliases": ["swift lang", "swiftui"]},
    "Kotlin":        {"category": "Programming Languages", "aliases": ["kotlin lang"]},
    "Scala":         {"category": "Programming Languages", "aliases": ["scala lang"]},
    "R":             {"category": "Programming Languages", "aliases": ["r language", "r programming", "rlang"]},
    "SQL":           {"category": "Programming Languages", "aliases": ["structured query language", "sql queries"]},
    "Bash":          {"category": "Programming Languages", "aliases": ["shell scripting", "shell script", "bash scripting"]},
    "MATLAB":        {"category": "Programming Languages", "aliases": ["matlab programming"]},
    "Perl":          {"category": "Programming Languages", "aliases": ["perl5", "perl scripting"]},
    "Dart":          {"category": "Programming Languages", "aliases": ["dart lang"]},

    # ── Web & Frameworks ─────────────────────────────────────
    "React":         {"category": "Web & Frameworks", "aliases": ["reactjs", "react.js", "react js"]},
    "Angular":       {"category": "Web & Frameworks", "aliases": ["angularjs", "angular.js", "angular 2"]},
    "Vue.js":        {"category": "Web & Frameworks", "aliases": ["vue", "vuejs", "vue 3"]},
    "Node.js":       {"category": "Web & Frameworks", "aliases": ["node", "nodejs", "node js"]},
    "Express":       {"category": "Web & Frameworks", "aliases": ["express.js", "expressjs", "express js"]},
    "Django":        {"category": "Web & Frameworks", "aliases": ["django framework", "django rest"]},
    "Flask":         {"category": "Web & Frameworks", "aliases": ["flask framework", "flask api"]},
    "FastAPI":       {"category": "Web & Frameworks", "aliases": ["fast api", "fastapi framework"]},
    "Spring Boot":   {"category": "Web & Frameworks", "aliases": ["springboot", "spring-boot", "spring framework"]},
    "Next.js":       {"category": "Web & Frameworks", "aliases": ["nextjs", "next js"]},
    "Svelte":        {"category": "Web & Frameworks", "aliases": ["sveltejs", "svelte js"]},
    "HTML":          {"category": "Web & Frameworks", "aliases": ["html5", "html 5"]},
    "CSS":           {"category": "Web & Frameworks", "aliases": ["css3", "css 3", "cascading style sheets"]},
    "Tailwind CSS":  {"category": "Web & Frameworks", "aliases": ["tailwind", "tailwindcss"]},
    "Bootstrap":     {"category": "Web & Frameworks", "aliases": ["bootstrap 5", "bootstrap css"]},
    "jQuery":        {"category": "Web & Frameworks", "aliases": ["jquery js"]},
    "GraphQL":       {"category": "Web & Frameworks", "aliases": ["graph ql", "graphql api"]},
    "REST API":      {"category": "Web & Frameworks", "aliases": ["restful api", "rest apis", "restful", "rest"]},
    "Flutter":       {"category": "Web & Frameworks", "aliases": ["flutter framework", "flutter sdk"]},
    "React Native":  {"category": "Web & Frameworks", "aliases": ["react-native", "reactnative"]},

    # ── Cloud & DevOps ───────────────────────────────────────
    "Docker":        {"category": "Cloud & DevOps", "aliases": ["docker container", "docker containers", "dockerfile"]},
    "Kubernetes":    {"category": "Cloud & DevOps", "aliases": ["k8s", "kube"]},
    "AWS":           {"category": "Cloud & DevOps", "aliases": ["amazon web services", "aws cloud"]},
    "GCP":           {"category": "Cloud & DevOps", "aliases": ["google cloud", "google cloud platform"]},
    "Azure":         {"category": "Cloud & DevOps", "aliases": ["microsoft azure", "azure cloud"]},
    "Terraform":     {"category": "Cloud & DevOps", "aliases": ["terraform iac", "hashicorp terraform"]},
    "Ansible":       {"category": "Cloud & DevOps", "aliases": ["ansible automation"]},
    "CI/CD":         {"category": "Cloud & DevOps", "aliases": ["cicd", "ci cd", "continuous integration", "continuous deployment"]},
    "Jenkins":       {"category": "Cloud & DevOps", "aliases": ["jenkins ci", "jenkins pipeline"]},
    "GitHub Actions":{"category": "Cloud & DevOps", "aliases": ["github-actions", "gh actions"]},
    "Linux":         {"category": "Cloud & DevOps", "aliases": ["linux admin", "linux administration", "unix"]},
    "Nginx":         {"category": "Cloud & DevOps", "aliases": ["nginx server"]},
    "Git":           {"category": "Cloud & DevOps", "aliases": ["git version control", "github", "gitlab"]},
    "Heroku":        {"category": "Cloud & DevOps", "aliases": ["heroku cloud"]},

    # ── Databases ────────────────────────────────────────────
    "MySQL":         {"category": "Databases", "aliases": ["my sql"]},
    "PostgreSQL":    {"category": "Databases", "aliases": ["postgres", "psql", "postgre sql"]},
    "MongoDB":       {"category": "Databases", "aliases": ["mongo", "mongo db"]},
    "Redis":         {"category": "Databases", "aliases": ["redis cache", "redis db"]},
    "SQLite":        {"category": "Databases", "aliases": ["sqlite3", "sqlite 3"]},
    "Oracle":        {"category": "Databases", "aliases": ["oracle db", "oracle database"]},
    "Cassandra":     {"category": "Databases", "aliases": ["apache cassandra"]},
    "Elasticsearch": {"category": "Databases", "aliases": ["elastic search", "elastic"]},
    "Firebase":      {"category": "Databases", "aliases": ["firebase db", "google firebase"]},
    "DynamoDB":      {"category": "Databases", "aliases": ["dynamo db", "aws dynamodb"]},

    # ── Data Science & ML ────────────────────────────────────
    "Pandas":        {"category": "Data Science & ML", "aliases": ["pandas library"]},
    "NumPy":         {"category": "Data Science & ML", "aliases": ["numpy library", "np"]},
    "Scikit-Learn":  {"category": "Data Science & ML", "aliases": ["sklearn", "scikit learn", "scikitlearn"]},
    "TensorFlow":    {"category": "Data Science & ML", "aliases": ["tensorflow 2", "tf"]},
    "PyTorch":       {"category": "Data Science & ML", "aliases": ["pytorch framework", "torch"]},
    "Keras":         {"category": "Data Science & ML", "aliases": ["keras api"]},
    "Data Analysis": {"category": "Data Science & ML", "aliases": ["data analytics", "analytical skills"]},
    "Machine Learning": {"category": "Data Science & ML", "aliases": ["ml", "machine-learning"]},
    "Deep Learning": {"category": "Data Science & ML", "aliases": ["dl", "deep-learning"]},
    "NLP":           {"category": "Data Science & ML", "aliases": ["natural language processing", "text mining"]},
    "Computer Vision": {"category": "Data Science & ML", "aliases": ["cv", "image processing"]},
    "Power BI":      {"category": "Data Science & ML", "aliases": ["powerbi", "power-bi"]},
    "Tableau":       {"category": "Data Science & ML", "aliases": ["tableau desktop", "tableau visualization"]},
    "Apache Spark":  {"category": "Data Science & ML", "aliases": ["spark", "pyspark"]},
    "Hadoop":        {"category": "Data Science & ML", "aliases": ["apache hadoop", "hadoop ecosystem"]},
    "Matplotlib":    {"category": "Data Science & ML", "aliases": ["matplotlib library"]},

    # ── Testing & QA ─────────────────────────────────────────
    "Unit Testing":  {"category": "Testing & QA", "aliases": ["unit tests", "unittest"]},
    "Selenium":      {"category": "Testing & QA", "aliases": ["selenium webdriver"]},
    "Jest":          {"category": "Testing & QA", "aliases": ["jest testing"]},
    "PyTest":        {"category": "Testing & QA", "aliases": ["pytest framework", "py.test"]},
    "Postman":       {"category": "Testing & QA", "aliases": ["postman api", "postman testing"]},

    # ── Soft Skills & Methodology ────────────────────────────
    "Agile":         {"category": "Soft Skills & Methodology", "aliases": ["agile methodology", "agile scrum"]},
    "Scrum":         {"category": "Soft Skills & Methodology", "aliases": ["scrum master", "scrum framework"]},
    "Team Leadership": {"category": "Soft Skills & Methodology", "aliases": ["leadership", "team lead", "team management"]},
    "Problem Solving": {"category": "Soft Skills & Methodology", "aliases": ["problem-solving", "analytical thinking"]},
    "Communication": {"category": "Soft Skills & Methodology", "aliases": ["verbal communication", "written communication", "communication skills"]},
    "Project Management": {"category": "Soft Skills & Methodology", "aliases": ["project planning", "project coordination"]},
    "Critical Thinking": {"category": "Soft Skills & Methodology", "aliases": ["critical-thinking", "analytical reasoning"]},
    "Time Management": {"category": "Soft Skills & Methodology", "aliases": ["time-management", "deadline management"]},
    "Collaboration":  {"category": "Soft Skills & Methodology", "aliases": ["teamwork", "team collaboration", "cross-functional"]},
}


def get_all_skill_names() -> list[str]:
    """Return a sorted list of all canonical skill names."""
    return sorted(SKILL_TAXONOMY.keys())


def get_categories() -> list[str]:
    """Return a sorted list of unique categories."""
    return sorted({v["category"] for v in SKILL_TAXONOMY.values()})


def get_skills_by_category(category: str) -> list[str]:
    """Return all canonical skill names belonging to a given category."""
    return sorted(
        name for name, info in SKILL_TAXONOMY.items()
        if info["category"] == category
    )


def get_aliases(skill_name: str) -> list[str]:
    """Return known aliases for a canonical skill name, or empty list."""
    entry = SKILL_TAXONOMY.get(skill_name)
    return entry["aliases"] if entry else []
