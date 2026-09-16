"""
recommendations.py — Intelligent Resume Recommendations & Gemini AI Integration
AI-Powered Resume & ATS Optimizer

Provides deep, actionable, domain-specific resume improvement bullet points,
keyword optimization strategies, and Google Gemini AI tailoring.
"""

from __future__ import annotations
import os
import requests
import json
from typing import Dict, List, Optional

# ──────────────────────────────────────────────────────────────
# CURATED HIGH-IMPACT RESUME BULLET POINTS FOR SKILLS
# Real-world, quantified bullet points with action verbs and impact metrics.
# ──────────────────────────────────────────────────────────────

CURATED_BULLET_POINTS: Dict[str, Dict[str, str]] = {
    # Cloud & DevOps
    "Docker": {
        "bullet": "Containerized multi-service web applications using Docker and Docker Compose, standardizing developer environments and reducing onboarding setup time by 60%.",
        "action": "Add to Technical Skills under Cloud/DevOps and include containerization details in a relevant project.",
    },
    "Kubernetes": {
        "bullet": "Architected Kubernetes deployment manifests with horizontal pod autoscaling and ingress routing, maintaining 99.9% application uptime across traffic spikes.",
        "action": "Highlight Kubernetes cluster orchestration, Helm charts, or cloud EKS/GKE management in your experience.",
    },
    "AWS": {
        "bullet": "Designed and deployed serverless cloud infrastructure on AWS (EC2, S3, Lambda, RDS), optimizing cloud expenditure by 25% using automated resource lifecycle policies.",
        "action": "Specify core AWS services (S3, EC2, Lambda) in both Skills and Experience sections to match ATS filters.",
    },
    "GCP": {
        "bullet": "Configured Google Cloud Platform (GCP) resources including Cloud Run, BigQuery, and Cloud Storage to support automated data pipelines with sub-second query latency.",
        "action": "List GCP along with specific services utilized in project descriptions.",
    },
    "Azure": {
        "bullet": "Provisioned enterprise Azure cloud environments utilizing Azure App Services, Blob Storage, and Azure DevOps CI/CD pipelines for automated zero-downtime releases.",
        "action": "Add Microsoft Azure certifications or project implementations prominently in your resume header or skills grid.",
    },
    "Terraform": {
        "bullet": "Automated multi-environment cloud infrastructure provisioning using Terraform (IaC), eliminating configuration drift and cutting environment rollout time from days to 15 minutes.",
        "action": "Mention Infrastructure as Code (IaC) and reusable Terraform modules in your engineering achievements.",
    },
    "CI/CD": {
        "bullet": "Built end-to-end CI/CD automation pipelines with automated linting, test suites, and Docker image builds, accelerating release cadence from bi-weekly to daily.",
        "action": "State CI/CD prominently alongside tool names like GitHub Actions, GitLab CI, or Jenkins.",
    },
    "GitHub Actions": {
        "bullet": "Developed reusable GitHub Actions workflows for automated code verification, security vulnerability scanning, and automated production deployments.",
        "action": "Detail GitHub Actions automation in your project bullet points to signal modern DevOps proficiency.",
    },
    "Linux": {
        "bullet": "Administered Linux production servers (Ubuntu/RHEL), writing shell scripts for system monitoring, log rotation, and automated cron task execution.",
        "action": "Include Linux command-line and systems administration under Technical Competencies.",
    },
    "Git": {
        "bullet": "Managed source control for distributed cross-functional teams using Git, enforcing PR code reviews, semantic versioning, and Gitflow branching strategies.",
        "action": "List Git in core toolchain and describe branch/merge conflict resolution workflows.",
    },

    # Data Science & Machine Learning
    "Machine Learning": {
        "bullet": "Engineered end-to-end machine learning pipelines from exploratory data analysis to feature engineering and model evaluation, improving prediction accuracy by 22%.",
        "action": "Quantify model metrics (AUC, F1-score, latency) in your ML project descriptions to validate expertise.",
    },
    "Deep Learning": {
        "bullet": "Trained deep neural network architectures using transfer learning and hyperparameter tuning, achieving state-of-the-art benchmark performance on custom domain datasets.",
        "action": "Specify frameworks (PyTorch/TensorFlow) and neural network architectures (CNNs, Transformers, ResNets).",
    },
    "Python": {
        "bullet": "Developed robust, modular backend services and automated data extraction scripts in Python, adhering to PEP 8 standards and achieving 90%+ unit test coverage.",
        "action": "Ensure Python is listed in the Primary Programming Languages section and referenced in recent roles.",
    },
    "Pandas": {
        "bullet": "Cleaned, aggregated, and transformed unstructured datasets exceeding 2M+ records using Pandas and NumPy, reducing memory footprint by 40% through vectorization.",
        "action": "Pair Pandas with data wrangling and analytics accomplishments in work history.",
    },
    "PyTorch": {
        "bullet": "Implemented and fine-tuned deep learning models in PyTorch with custom loss functions and GPU-accelerated training using CUDA.",
        "action": "Include PyTorch in project bullet points with explicit training hardware or dataset details.",
    },
    "TensorFlow": {
        "bullet": "Trained and deployed production deep learning models utilizing TensorFlow and Keras, exporting lightweight models for low-latency inference.",
        "action": "List TensorFlow under Frameworks & Libraries and mention deployment details.",
    },
    "Scikit-Learn": {
        "bullet": "Implemented supervised and unsupervised classification algorithms in Scikit-Learn, conducting cross-validation and feature importance analysis.",
        "action": "Mention specific algorithms (Random Forest, XGBoost, SVM) utilized via Scikit-Learn.",
    },
    "NLP": {
        "bullet": "Designed Natural Language Processing (NLP) solutions for sentiment classification and entity extraction using tokenization, TF-IDF, and transformer embeddings.",
        "action": "Spell out 'Natural Language Processing (NLP)' so both full term and acronym are picked up by ATS scanners.",
    },
    "LLM": {
        "bullet": "Architected generative AI applications integrating Large Language Models (LLMs) via prompt engineering, few-shot examples, and Retrieval-Augmented Generation (RAG).",
        "action": "Highlight RAG workflows, vector databases, or LLM fine-tuning in contemporary projects.",
    },

    # Databases
    "PostgreSQL": {
        "bullet": "Architected normalized relational database schemas in PostgreSQL, writing complex indexed queries and CTEs that decreased API query response times by 45%.",
        "action": "Detail query optimization, indexing, or transaction management in PostgreSQL.",
    },
    "MySQL": {
        "bullet": "Designed high-performance MySQL schemas, implementing composite indexing and connection pooling to support 10,000+ concurrent user queries.",
        "action": "Include MySQL in Database section and reference database tuning in bullet points.",
    },
    "MongoDB": {
        "bullet": "Structured flexible NoSQL document schemas in MongoDB, utilizing aggregation pipelines to deliver real-time operational analytics dashboards.",
        "action": "Mention document modeling, aggregation pipelines, and indexing in MongoDB.",
    },
    "Redis": {
        "bullet": "Implemented high-speed caching and session management layers using Redis, reducing database load by 65% and cutting average endpoint response times to <50ms.",
        "action": "Pair Redis with caching strategies, distributed locks, or pub/sub messaging in experience bullets.",
    },
    "SQL": {
        "bullet": "Formulated complex analytical SQL queries involving window functions, multi-table joins, and stored procedures to generate executive operational metrics.",
        "action": "Ensure SQL is prominent; specify dialects (PostgreSQL, MySQL, T-SQL) for ATS scoring.",
    },

    # Web & Frameworks
    "React": {
        "bullet": "Built responsive single-page applications (SPAs) with React, React Hooks, and Redux, improving Core Web Vitals and cutting initial page load times by 35%.",
        "action": "Mention React along with state management (Redux/Zustand) and modern component architecture.",
    },
    "Next.js": {
        "bullet": "Developed server-side rendered (SSR) and statically generated web applications with Next.js and TypeScript, optimizing SEO indexation and client performance.",
        "action": "Highlight SSR/SSG benefits and performance gains delivered with Next.js.",
    },
    "Node.js": {
        "bullet": "Constructed asynchronous RESTful microservices in Node.js and Express, implementing JWT authentication and rate limiting for secure API access.",
        "action": "Include Node.js in backend engineering projects alongside Express or NestJS.",
    },
    "FastAPI": {
        "bullet": "Engineered high-throughput asynchronous REST APIs using FastAPI and Pydantic, providing automatic OpenAPI documentation and sub-20ms endpoint latency.",
        "action": "Highlight async programming (async/await) and data validation with FastAPI.",
    },
    "Django": {
        "bullet": "Developed full-stack web applications using Django and Django REST Framework (DRF), incorporating ORM optimization, Celery background tasks, and user authentication.",
        "action": "Mention Django ORM, REST Framework, and background task queues.",
    },
    "TypeScript": {
        "bullet": "Migrated legacy JavaScript codebases to strictly-typed TypeScript, catching runtime edge cases during compilation and improving team maintainability.",
        "action": "List TypeScript as a primary language and emphasize type safety in project work.",
    },
    "JavaScript": {
        "bullet": "Developed interactive, cross-browser web interfaces utilizing ES6+ JavaScript, asynchronous promises, and DOM event handling.",
        "action": "Ensure JavaScript (ES6+) is featured under Frontend Development.",
    },
    "HTML5": {
        "bullet": "Structured semantic, accessible (WCAG 2.1 compliant) web layouts utilizing modern HTML5 elements and responsive viewport configurations.",
        "action": "Pair HTML5 with semantic markup and accessibility in skills inventory.",
    },
    "CSS3": {
        "bullet": "Created modular, responsive styling layouts using CSS3 Flexbox, CSS Grid, and custom CSS variables across desktop and mobile form factors.",
        "action": "Combine CSS3 with responsive design or utility frameworks in project bullets.",
    },
    "Tailwind CSS": {
        "bullet": "Implemented modern, cohesive UI design systems using Tailwind CSS utility classes, speeding up feature UI prototyping by 50%.",
        "action": "Highlight design system consistency and rapid layout styling with Tailwind CSS.",
    },

    # Testing & Methodology
    "Unit Testing": {
        "bullet": "Authored comprehensive unit and integration test suites achieving 85%+ test coverage, integrating automated test runners into pre-commit and CI hooks.",
        "action": "Quantify test coverage percentages in your projects to prove software reliability.",
    },
    "PyTest": {
        "bullet": "Developed automated test fixtures and parameterized test suites using PyTest and mock libraries to validate critical business logic and API contracts.",
        "action": "Mention PyTest alongside Python backend testing in experience descriptions.",
    },
    "Agile": {
        "bullet": "Collaborated in Agile/Scrum sprints with bi-weekly iterations, participating in sprint planning, backlog grooming, and daily stand-ups to deliver features on time.",
        "action": "Include Agile development and cross-functional sprint collaboration in experience summary.",
    },
    "Problem Solving": {
        "bullet": "Diagnosed and resolved complex production bottleneck issues, analyzing APM telemetry and log streams to identify root causes and implement permanent fixes.",
        "action": "Illustrate problem solving with concrete troubleshooting or algorithmic optimization stories.",
    },
}


def get_skill_recommendation(skill_name: str, category: str = "General") -> Dict[str, str]:
    """
    Get detailed, realistic recommendations for a specific skill.
    If the skill is in our curated library, return the curated data.
    Otherwise, generate a domain-aware, professional template (never random gibberish).
    """
    if skill_name in CURATED_BULLET_POINTS:
        return CURATED_BULLET_POINTS[skill_name]

    # Domain-aware fallback generator
    cat_lower = category.lower()
    if "cloud" in cat_lower or "devops" in cat_lower:
        bullet = f"Implemented and maintained automated cloud workflows utilizing {skill_name}, improving deployment reliability and operational monitoring."
        action = f"Add {skill_name} under Technical Skills (Cloud & Infrastructure) and highlight in deployment experience."
    elif "data" in cat_lower or "ml" in cat_lower or "ai" in cat_lower:
        bullet = f"Leveraged {skill_name} for predictive modeling and data processing, analyzing complex data structures to extract actionable business insights."
        action = f"Incorporate {skill_name} into your Data Science/ML projects with specific evaluation metrics."
    elif "database" in cat_lower or "storage" in cat_lower:
        bullet = f"Managed data persistence and querying operations using {skill_name}, designing efficient schemas and optimizing query performance."
        action = f"List {skill_name} under Database Technologies and specify schema design or query optimization work."
    elif "web" in cat_lower or "front" in cat_lower:
        bullet = f"Engineered intuitive and performant user interface components using {skill_name}, enhancing user engagement and cross-device responsiveness."
        action = f"Feature {skill_name} in your Frontend Development stack with live project links or screenshots."
    elif "program" in cat_lower or "language" in cat_lower:
        bullet = f"Developed scalable backend services and algorithmic modules in {skill_name}, focusing on clean architecture, modular design, and robust error handling."
        action = f"Add {skill_name} to your Core Programming Languages list and reference in your most recent project."
    elif "test" in cat_lower or "qa" in cat_lower:
        bullet = f"Designed comprehensive automated testing suites utilizing {skill_name}, verifying edge cases and maintaining high code reliability across releases."
        action = f"Include {skill_name} under Quality Assurance & Testing in your technical summary."
    else:
        bullet = f"Applied {skill_name} to optimize project workflows, collaborating with cross-functional teams to execute deliverables on schedule."
        action = f"Add {skill_name} to your Technical Skills section and mention in relevant work experience bullet points."

    return {
        "bullet": bullet,
        "action": action,
    }


# ──────────────────────────────────────────────────────────────
# CURATED TECHNICAL INTERVIEW QUESTIONS & PIVOT STRATEGIES
# Deep screening questions, probing intent, and gap-defense talking points.
# ──────────────────────────────────────────────────────────────

CURATED_INTERVIEW_QUESTIONS: Dict[str, Dict[str, str]] = {
    "Docker": {
        "question": "How do you optimize Docker image sizes for production, and what strategies do you use for layer caching and multi-stage builds?",
        "intent": "Assesses containerization best practices, image security (non-root users, distroless), and CI/CD build speeds.",
        "pivot": "Acknowledge virtualization experience in local development/virtual environments, and explain conceptual mastery of multi-stage Dockerfiles and container lifecycle.",
        "key_terms": "Multi-stage builds, layer caching, Alpine/distroless, non-root user, .dockerignore",
    },
    "Kubernetes": {
        "question": "How does Kubernetes handle self-healing, rolling updates, and service discovery? When would you use a DaemonSet versus a Deployment?",
        "intent": "Evaluates cluster administration depth, rollout safety (Readiness/Liveness probes), and microservice traffic management.",
        "pivot": "Bridge experience from Docker Compose or managed cloud containers (AWS ECS/Cloud Run), highlighting container orchestration architecture concepts.",
        "key_terms": "Liveness/Readiness probes, HPA, RollingUpdate, ConfigMaps, Ingress controller",
    },
    "AWS": {
        "question": "Walk me through how you would architect a highly available, auto-scaling web application on AWS with secure networking and least-privilege IAM.",
        "intent": "Tests multi-tier cloud design: VPC subnets, ELB, Auto Scaling, RDS Multi-AZ, and S3/CloudFront caching.",
        "pivot": "Translate concepts from another cloud provider (GCP/Azure) or Linux on-prem servers, emphasizing that VPC, subnets, and IAM principles are universal.",
        "key_terms": "VPC, Public/Private subnets, IAM least privilege, Auto Scaling Groups, Multi-AZ RDS, CloudFront",
    },
    "GCP": {
        "question": "How do you leverage GCP Cloud Run, BigQuery, and IAM Service Accounts to design automated serverless data processing pipelines?",
        "intent": "Tests serverless compute paradigms, BigQuery partitioned tables, and secure GCP IAM authentication.",
        "pivot": "Connect cloud experience from AWS or Azure, demonstrating that serverless containers and analytical data warehouses operate on identical principles.",
        "key_terms": "Cloud Run, BigQuery partitioning, Service Accounts, Pub/Sub, Cloud Storage",
    },
    "Azure": {
        "question": "How do you configure Azure App Services and Virtual Networks for zero-downtime blue/green deployment slots?",
        "intent": "Evaluates Azure enterprise architecture, deployment slots, and VNet integration.",
        "pivot": "Highlight transferable infrastructure experience with cloud networking, managed apps, and automated zero-downtime deployment pipelines.",
        "key_terms": "Deployment slots, VNet integration, Azure Key Vault, App Service Plans",
    },
    "Terraform": {
        "question": "How do you manage remote state locking in Terraform, and how do you prevent configuration drift in collaborative teams?",
        "intent": "Tests Infrastructure as Code (IaC) governance, S3/DynamoDB state locking, workspaces, and reusable modules.",
        "pivot": "Explain scripting and infrastructure automation principles, emphasizing the benefits of version-controlled, declarative infrastructure.",
        "key_terms": "Remote backend, state locking, terraform plan/apply, modules, drift detection",
    },
    "CI/CD": {
        "question": "How do you structure a production-grade CI/CD pipeline with automated linting, test suites, artifact building, and zero-downtime rollback capabilities?",
        "intent": "Assesses automation mindset, quality gates, immutable artifact promotion, and deployment reliability.",
        "pivot": "Emphasize Git version control hygiene, automated test scripts, and experience triggering deployment workflows.",
        "key_terms": "Automated test gates, immutable artifacts, blue-green deployment, canary releases, rollbacks",
    },
    "GitHub Actions": {
        "question": "How do you design reusable composite GitHub Actions workflows with secrets management and automated environment deployment approvals?",
        "intent": "Assesses modern workflow orchestration, matrix builds, runner management, and OIDC authentication.",
        "pivot": "Connect familiarity with shell scripting and automated testing, demonstrating understanding of event-driven automation triggers.",
        "key_terms": "Composite actions, matrix builds, OIDC, workflow_dispatch, branch protection",
    },
    "Git": {
        "question": "Explain the difference between git merge, git rebase, and squash merging. How do you resolve merge conflicts across diverged branches?",
        "intent": "Assesses collaborative team workflows, linear commit history, and source control discipline.",
        "pivot": "Highlight disciplined pull request workflows, descriptive semantic commit messages, and branch protection practices.",
        "key_terms": "Rebase vs merge, interactive rebase, fast-forward, merge conflict resolution, cherry-pick",
    },
    "Linux": {
        "question": "How do you investigate high CPU, memory, or disk I/O bottlenecks on a Linux server using CLI tools, and how do file permissions and systemd services work?",
        "intent": "Tests practical sysadmin diagnostics: top/htop, iotop, netstat/ss, journalctl, and process management.",
        "pivot": "State comfort working in POSIX/Bash environments, administering servers, and reading system logs for root-cause diagnosis.",
        "key_terms": "systemd, journalctl, top/htop, lsof, chmod/chown, memory swappiness",
    },
    "Python": {
        "question": "How does Python's Global Interpreter Lock (GIL) influence concurrent execution, and how do you choose between asyncio, threading, and multiprocessing?",
        "intent": "Tests deep understanding of Python memory management, I/O-bound vs. CPU-bound concurrency, and the asyncio event loop.",
        "pivot": "Highlight clean, idiomatic Python (PEP 8, type hints, generators) and proven experience designing REST APIs and automated data pipelines.",
        "key_terms": "GIL, asyncio event loop, multiprocessing vs threading, CPU-bound vs I/O-bound, generators",
    },
    "FastAPI": {
        "question": "How does FastAPI leverage Python type hints and Pydantic for automated request validation, and how does ASGI support high concurrency?",
        "intent": "Evaluates modern async Python API architecture, dependency injection, and OpenAPI standards.",
        "pivot": "Connect REST API design patterns from Flask or Django, highlighting understanding of HTTP verbs, status codes, and serialization.",
        "key_terms": "ASGI, Pydantic models, async/await, dependency injection, OpenAPI documentation",
    },
    "Django": {
        "question": "How do you optimize database access in the Django ORM to avoid the N+1 queries problem using select_related and prefetch_related?",
        "intent": "Assesses ORM query evaluation, transaction middleware, migrations, and caching.",
        "pivot": "Discuss MVC/MVT architecture, relational database modeling, and backend web frameworks.",
        "key_terms": "select_related, prefetch_related, ORM indexing, Django migrations, middleware",
    },
    "React": {
        "question": "How does React's Virtual DOM diffing algorithm work, and how do you prevent re-rendering bottlenecks using useMemo, useCallback, and React.memo?",
        "intent": "Tests frontend performance optimization, reconciliation, hook rules, and state management architectures.",
        "pivot": "Demonstrate strong fundamentals in modern ES6+ JavaScript, DOM events, and component-driven UI architecture.",
        "key_terms": "Virtual DOM diffing, reconciliation, useMemo, useCallback, React.memo, custom hooks",
    },
    "Next.js": {
        "question": "Explain the architectural differences between Server-Side Rendering (SSR), Static Site Generation (SSG), and Server Components (RSC) in Next.js.",
        "intent": "Tests modern full-stack rendering pipelines, SEO indexation, hydration, and cache revalidation.",
        "pivot": "Connect frontend single-page application principles with server performance, discussing client vs server boundaries.",
        "key_terms": "SSR, SSG, React Server Components (RSC), hydration, incremental static regeneration (ISR)",
    },
    "Node.js": {
        "question": "Explain the phases of the Node.js event loop (Timers, Poll, Check) and how libuv handles asynchronous non-blocking I/O.",
        "intent": "Tests runtime engine understanding, microtask vs macrotask execution order, and preventing CPU-bound thread blocking.",
        "pivot": "Highlight backend API design experience in Python/Java/Go, discussing microservices, asynchronous handlers, and REST best practices.",
        "key_terms": "libuv, event loop phases, process.nextTick, streams, non-blocking I/O, clustering",
    },
    "TypeScript": {
        "question": "How do TypeScript interfaces differ from type aliases, and how do Generics, Discriminated Unions, and utility types (Partial, Pick) enhance codebase safety?",
        "intent": "Tests structural typing, compile-time type inference, and reducing runtime production crashes.",
        "pivot": "Emphasize deep mastery of JavaScript (ES6+), component structure, and strong enthusiasm for static type verification.",
        "key_terms": "Generics, discriminated unions, utility types (Pick/Omit), structural typing, type narrowing",
    },
    "JavaScript": {
        "question": "Explain how closures, prototypical inheritance, and event bubbling/capturing work in JavaScript, and what the difference is between Event Loop microtasks and macrotasks.",
        "intent": "Tests fundamental JavaScript language mechanics beyond surface framework syntax.",
        "pivot": "Highlight core programming fundamentals, asynchronous promise handling, and DOM interaction proficiency.",
        "key_terms": "Closures, prototype chain, event delegation, Promises, microtask queue",
    },
    "SQL": {
        "question": "How do B-Tree indexes function under the hood, and how do you use EXPLAIN ANALYZE to detect table scans, sequential scans, or suboptimal joins?",
        "intent": "Tests query execution optimization, indexing tradeoffs (read speed vs write amplification), and locking.",
        "pivot": "Discuss solid experience writing complex joins, CTEs, and aggregation queries, along with disciplined schema normalization.",
        "key_terms": "B-Tree index, EXPLAIN ANALYZE, composite indexes, query plan, write amplification, normalization",
    },
    "PostgreSQL": {
        "question": "Explain Multi-Version Concurrency Control (MVCC) in PostgreSQL. How do vacuuming, table bloat, and connection pooling affect high-throughput applications?",
        "intent": "Evaluates relational database internals, transaction isolation levels, and operational maintenance under load.",
        "pivot": "Demonstrate strong relational schema design in MySQL/SQL, emphasizing ACID compliance and index tuning.",
        "key_terms": "MVCC, autovacuum, connection pooling (PgBouncer), CTEs, JSONB data types",
    },
    "MySQL": {
        "question": "How does InnoDB handle row-level locking, and what causes deadlocks during concurrent multi-row transactions?",
        "intent": "Assesses relational storage engine internals, ACID transactions, and index seek mechanics.",
        "pivot": "Demonstrate relational modeling, transaction management, and indexing skills across SQL databases.",
        "key_terms": "InnoDB, Clustered index, ACID, deadlocks, transaction isolation",
    },
    "MongoDB": {
        "question": "When designing MongoDB schemas, how do you decide between embedding vs referencing documents, and how do aggregation pipelines scale with indexes?",
        "intent": "Tests document modeling tradeoffs (16MB BSON limit, atomicity) and performance optimization in NoSQL databases.",
        "pivot": "Explain familiarity with JSON data structures, schema-on-read principles, and query optimization from relational or document stores.",
        "key_terms": "Embedding vs referencing, aggregation pipeline, compound indexes, replica sets, sharding",
    },
    "Redis": {
        "question": "What caching strategies (Cache-Aside, Write-Through) do you employ with Redis, and how do you prevent cache stampedes and memory exhaustion?",
        "intent": "Assesses in-memory data structures, TTL management, eviction policies (LRU/LFU), and distributed caching.",
        "pivot": "Discuss application-level caching, query caching, and HTTP caching, explaining how Redis acts as an ultra-low latency key-value layer.",
        "key_terms": "Cache-Aside pattern, TTL, LRU eviction, Redis Hashes, cache stampede / thundering herd",
    },
    "Machine Learning": {
        "question": "How do you detect and prevent data leakage in ML training pipelines, and how do you choose evaluation metrics (F1-score, PR-AUC) for skewed classes?",
        "intent": "Evaluates end-to-end ML rigor, cross-validation isolation, feature engineering, and model evaluation.",
        "pivot": "Walk through disciplined data preprocessing, statistical validation, model benchmarking, and translating ML predictions into business impact.",
        "key_terms": "Data leakage, stratified k-fold, PR-AUC vs ROC-AUC, feature importance, regularization",
    },
    "Deep Learning": {
        "question": "How do you diagnose vanishing/exploding gradients during neural network training, and what strategies (batch norm, residual connections, learning rate schedulers) mitigate them?",
        "intent": "Tests neural network backpropagation, architecture selection (Transformers vs CNNs), and training stability.",
        "pivot": "Focus on machine learning foundations, feature representations, and transfer learning workflows using modern frameworks.",
        "key_terms": "Vanishing gradients, Batch Normalization, AdamW optimizer, Residual connections, Cosine annealing",
    },
    "PyTorch": {
        "question": "Explain how PyTorch's dynamic computational graph (Autograd) works, and how you profile GPU memory to avoid CUDA Out-of-Memory (OOM) errors.",
        "intent": "Evaluates practical PyTorch tensor operations, gradient accumulation, mixed precision (AMP), and distributed data parallel (DDP).",
        "pivot": "Describe hands-on Python data manipulation, vectorization, and model training methodologies.",
        "key_terms": "Autograd, torch.no_grad(), Mixed Precision (AMP), gradient accumulation, DataLoader pin_memory",
    },
    "Pandas": {
        "question": "How do you optimize Pandas performance for multi-million row datasets to eliminate memory bottlenecks and avoid SettingWithCopyWarning?",
        "intent": "Tests vectorization vs iterrows, downcasting datatypes (category, int32), and efficient aggregation groupby methods.",
        "pivot": "Discuss data processing rigor, algorithmic complexity, and structured ETL pipeline design.",
        "key_terms": "Vectorization, downcasting datatypes, chunking, groupby-agg, loc vs iloc",
    },
    "NLP": {
        "question": "What are the key architectural tradeoffs between traditional TF-IDF/N-gram models versus modern Transformer self-attention for text classification?",
        "intent": "Tests computational cost vs semantic context, positional embeddings, and fine-tuning strategies.",
        "pivot": "Highlight text preprocessing fundamentals, tokenization, regular expression extraction, and domain-specific lexicon design.",
        "key_terms": "Self-attention mechanism, subword tokenization (BPE), contextual embeddings, cosine similarity, inference latency",
    },
    "REST API": {
        "question": "What constitutes an idempotent HTTP method in REST, and how do you design versioning, pagination, and standardized error schemas?",
        "intent": "Evaluates HTTP status code conventions, cursor vs offset pagination, and API security (rate limiting, CORS).",
        "pivot": "Discuss clean endpoint naming conventions, JSON serialization, and contract-first API design.",
        "key_terms": "Idempotency (GET/PUT/DELETE vs POST), HTTP 4xx vs 5xx, cursor pagination, rate limiting",
    },
}


def get_skill_interview_details(skill_name: str, category: str = "") -> Dict[str, str]:
    """
    Retrieve curated interview questions, probing intent, pivot strategies,
    and key terminology for a given skill.
    """
    if skill_name in CURATED_INTERVIEW_QUESTIONS:
        return CURATED_INTERVIEW_QUESTIONS[skill_name]

    cat_lower = category.lower() if category else ""
    if "cloud" in cat_lower or "devops" in cat_lower:
        question = f"Describe your approach to deploying, monitoring, and scaling infrastructure with {skill_name} in production."
        intent = f"Evaluates practical deployment experience, zero-downtime strategies, and monitoring with {skill_name}."
        pivot = f"Highlight fundamental infrastructure and networking principles, explaining how you apply similar automation practices with {skill_name}."
        key_terms = f"{skill_name}, automated deployments, health checks, monitoring, rollback strategy"
    elif "data" in cat_lower or "ml" in cat_lower or "ai" in cat_lower:
        question = f"How have you utilized {skill_name} for data transformations, model training, or analytical benchmarking?"
        intent = f"Tests analytical rigor, algorithmic trade-offs, and computational efficiency using {skill_name}."
        pivot = f"Emphasize strong data cleaning, exploratory analysis, and how you rapidly adopt specialized libraries like {skill_name}."
        key_terms = f"{skill_name}, data pipelines, benchmarking, validation, optimization"
    elif "database" in cat_lower or "storage" in cat_lower:
        question = f"How do you approach schema design, data consistency, and query optimization when utilizing {skill_name}?"
        intent = f"Assesses understanding of storage engines, indexing strategies, and concurrency in {skill_name}."
        pivot = f"Demonstrate deep comprehension of data integrity, query optimization, and how core database concepts map directly to {skill_name}."
        key_terms = f"{skill_name}, indexing, ACID/BASE, query latency, connection management"
    elif "web" in cat_lower or "framework" in cat_lower:
        question = f"What architectural patterns, state management, and performance considerations do you prioritize when building with {skill_name}?"
        intent = f"Tests component or service modularity, lifecycle management, and API design in {skill_name}."
        pivot = f"Connect architecture patterns from other frameworks, focusing on modularity, testability, and clean separation of concerns."
        key_terms = f"{skill_name}, component architecture, state management, REST/API, responsive design"
    elif "programming" in cat_lower or "language" in cat_lower:
        question = f"What are the key memory management, concurrency, and performance characteristics of {skill_name}?"
        intent = f"Differentiates basic syntax knowledge from deep systems-level comprehension in {skill_name}."
        pivot = f"Demonstrate strong algorithmic problem solving, clean code standards, and rapid ramp-up in any programming syntax."
        key_terms = f"{skill_name}, memory management, concurrency, unit testing, clean architecture"
    else:
        question = f"How do you leverage {skill_name} to drive project delivery, optimize workflows, and maintain engineering quality?"
        intent = f"Tests practical application and problem-solving maturity with {skill_name}."
        pivot = f"Highlight transferable problem-solving skills, structured workflow management, and quick adoption of {skill_name}."
        key_terms = f"{skill_name}, best practices, collaboration, delivery, documentation"

    return {
        "question": question,
        "intent": intent,
        "pivot": pivot,
        "key_terms": key_terms,
    }


def call_gemini_api(
    prompt: str,
    api_key: str,
    model: str = "gemini-2.5-flash",
    temperature: float = 0.2,
    max_output_tokens: int = 3000,
) -> str:
    """
    Call Google Gemini API with automatic model fallback, temperature=0.2,
    and robust error handling for quota limits, invalid keys, and network timeouts.
    """
    if not api_key or not api_key.strip():
        return "Error: No Gemini API Key provided."

    clean_key = api_key.strip()
    # Candidate models in priority order
    candidate_models = [model, "gemini-3.6-flash", "gemini-flash-latest", "gemini-3.1-flash-lite"]
    # De-duplicate while preserving order
    seen = set()
    models_to_try = []
    for m in candidate_models:
        if m and m not in seen:
            seen.add(m)
            models_to_try.append(m)

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
        }
    }
    headers = {"Content-Type": "application/json"}

    last_error = ""
    for current_model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{current_model}:generateContent?key={clean_key}"
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=55)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        text_chunks = [p.get("text", "") for p in parts if "text" in p]
                        return "".join(text_chunks).strip()
                return "Gemini returned an empty response. Please retry."
            elif response.status_code == 404:
                # Model deprecated or unavailable for this key, try next model
                last_error = f"Model {current_model} not available (404)."
                continue
            elif response.status_code == 400:
                last_error = f"Gemini API Error (400 Invalid Request): {response.text[:200]}"
                continue
            elif response.status_code == 403:
                return "API Error: Invalid API key or permission denied."
            elif response.status_code == 429:
                return "Gemini API Rate Limit / Quota Exceeded: Please wait a moment and try again."
            else:
                last_error = f"Gemini API Error ({response.status_code}): {response.text[:200]}"
        except requests.exceptions.Timeout:
            last_error = "Gemini API Request Timed Out (55s). Please check network connection and try again."
            break
        except requests.exceptions.RequestException as e:
            last_error = f"Gemini Network Error: {str(e)}"
            break

    return last_error or "Failed to generate content from Gemini API."


import re

def parse_gemini_sections(text: str) -> Dict[str, str]:
    """
    Parse the structured 5-section recruiter audit into clean components
    for rendering in dedicated Streamlit tabs.
    """
    sections = {
        "raw": text,
        "executive_overview": "",
        "technical_matrix": "",
        "project_depth": "",
        "bullet_rewrites": "",
        "interview_questions": "",
    }

    if not text or text.startswith("Gemini API Error") or text.startswith("Error:"):
        return sections

    patterns = [
        ("executive_overview", r"(?:##\s*1\.?\s*Candidate\s*Executive\s*Overview)([\s\S]*?)(?=##\s*2\.|\Z)"),
        ("technical_matrix", r"(?:##\s*2\.?\s*Technical\s*&\s*Domain\s*Alignment\s*Matrix)([\s\S]*?)(?=##\s*3\.|\Z)"),
        ("project_depth", r"(?:##\s*3\.?\s*Project\s*&\s*Impact\s*Depth\s*Audit)([\s\S]*?)(?=##\s*4\.|\Z)"),
        ("bullet_rewrites", r"(?:##\s*4\.?\s*Actionable\s*Bullet-Point\s*Rewrites)([\s\S]*?)(?=##\s*5\.|\Z)"),
        ("interview_questions", r"(?:##\s*5\.?\s*(?:Critical\s*)?(?:Technical\s*)?Interview[\s\S]*?)([\s\S]*?)(?=\Z)"),
    ]

    for key, pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            sections[key] = match.group(1).strip()

    # Fallback search if interview_questions didn't match the strict regex
    if not sections["interview_questions"] and text:
        match_5 = re.search(r"(?:##\s*5\.?[\s\S]*?)([\s\S]*?)(?=\Z)", text, re.IGNORECASE)
        if match_5:
            sections["interview_questions"] = match_5.group(1).strip()
        else:
            match_iq = re.search(r"(?:Interview\s*Readiness[\s\S]*?)([\s\S]*?)(?=\Z)", text, re.IGNORECASE)
            if match_iq:
                sections["interview_questions"] = match_iq.group(1).strip()

    return sections


def generate_full_gemini_audit(
    resume_text: str,
    jd_text: str,
    api_key: str,
    model: str = "gemini-2.5-flash",
) -> Dict[str, str]:
    """
    Perform an exhaustive line-by-line semantic evaluation of the Candidate Resume
    against the Target Job Description with temperature=0.2.
    Returns parsed sections and complete recruiter markdown audit.
    """
    prompt = f"""You are a Principal Technical Recruiter and Chief ATS Systems Architect.
Perform an exhaustive line-by-line semantic evaluation of the Candidate Resume against the Target Job Description.
Output a concrete, recruiter-grade breakdown without generic conversational filler.

========================
TARGET JOB DESCRIPTION:
========================
{jd_text}

========================
CANDIDATE RESUME:
========================
{resume_text}

========================
INSTRUCTIONS & REQUIRED SECTIONS:
========================
Format your output in clean Markdown using the following exact section headers and sub-headers:

## 1. Candidate Executive Overview
- **Candidate Full Name**: [Extract full name from resume]
- **Target Role Title**: [Extract target role from JD]
- **Experience Detected vs Required**: [e.g., 6 years detected vs 5+ years required by JD]
- **Core Competency Summary**: [2-3 direct, punchy sentences summarizing actual candidate readiness, primary strengths, and critical domain posture]

## 2. Technical & Domain Alignment Matrix
### Must-Have Skills (Directly Met with Quoted Resume Evidence)
- [List explicitly met requirements with exact quoted phrases/evidence from the resume]
### Core Missing Competencies (Hard Gaps)
- [List hard gaps in tools, libraries, infrastructure, or architecture explicitly demanded by the JD that the candidate completely lacks]
### Partial / Adjacent Matches
- [List related technologies the candidate knows that can legitimately substitute or translate to the JD requirements, with technical rationale]

## 3. Project & Impact Depth Audit
- **Production-Ready vs Academic Assessment**: [Evaluate whether candidate projects demonstrate real production scale, distributed systems, and real users vs superficial academic coursework]
- **Quantifiable Metrics Check**: [Audit presence or absence of quantifiable engineering metrics such as latency reduction, throughput, scale, uptime, or business impact]
- **Weak / Passive Verbs Identified**: [Highlight occurrences of weak verbs such as 'worked on', 'assisted with', 'handled', 'helped', and pinpoint where they appear in the resume]

## 4. Actionable Bullet-Point Rewrites (Google XYZ Formula)
Select 2-3 weak or generic bullet points directly from the candidate's resume and provide an optimized rewrite for each using the Google XYZ formula ("Accomplished [X] as measured by [Y], by doing [Z]"), tailored specifically to the keywords and phrasing of the target Job Description.

### Bullet 1
- **Original**: [Exact quote of weak bullet point from resume]
- **Optimized Rewrite**: Accomplished [X] as measured by [Y], by doing [Z]

### Bullet 2
- **Original**: [Exact quote of second weak bullet point from resume]
- **Optimized Rewrite**: Accomplished [X] as measured by [Y], by doing [Z]

### Bullet 3
- **Original**: [Exact quote of third weak bullet point from resume if available]
- **Optimized Rewrite**: Accomplished [X] as measured by [Y], by doing [Z]

## 5. Critical Interview Readiness Questions
Generate 3 rigorous, high-pressure technical interview questions the candidate will likely face to test the weak or questionable spots identified during this scan. Include brief coaching notes on what recruiters/interviewers are looking for.
1. [Question 1 targeting a specific skill or architectural gap]
2. [Question 2 targeting depth of implementation or scale]
3. [Question 3 targeting design tradeoffs or missing competencies]
"""

    raw_output = call_gemini_api(
        prompt=prompt,
        api_key=api_key,
        model=model,
        temperature=0.2,
        max_output_tokens=3200,
    )

    parsed = parse_gemini_sections(raw_output)
    return parsed


# Backwards compatibility wrappers
def compare_resume_with_jd_gemini(
    resume_text: str,
    jd_text: str,
    api_key: str,
    model: str = "gemini-2.5-flash",
) -> str:
    audit_dict = generate_full_gemini_audit(resume_text, jd_text, api_key, model=model)
    return audit_dict.get("raw", "")


def get_gemini_tailored_optimization(
    resume_text: str,
    jd_text: str,
    missing_skills: List[str],
    api_key: str,
    model: str = "gemini-2.5-flash",
) -> str:
    audit_dict = generate_full_gemini_audit(resume_text, jd_text, api_key, model=model)
    return audit_dict.get("raw", "")


