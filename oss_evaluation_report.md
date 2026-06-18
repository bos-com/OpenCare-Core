# Open Source Evaluation — OpenCare-Core

**Repository:** `bos-com/OpenCare-Core`
**Snapshot date:** 29 April 2026
**Author:** Coursework submission

This file is one of four sibling reports — each in its own repository — that together evaluate the four flagship Bugema Open Source Community (BOSC) projects against open source principles. The companion files live in `bos-com/GreenCode`, `bos-com/LifeLine-ICT`, and `bos-com/BOS`. Every claim below is grounded in publicly verifiable evidence from this repository, the BOSC organisation profile, and the `bos-com/bosc-governance` repository, captured on the snapshot date above.

## 1. Evaluation framework

Six principles are applied (drawn from the OSI Open Source Definition, GitHub's Open Source Guides, and CHAOSS community-health metrics):

1. **Recognised licence at root.**
2. **README covers purpose, scope, and setup.**
3. **Explicit project-level governance** (CONTRIBUTING, CODE_OF_CONDUCT, GOVERNANCE).
4. **Inclusive contribution workflow** (issue/PR templates, labels, "good first issue").
5. **Active maintenance and review velocity.**
6. **Code of conduct + security policy at repo level.**

Each principle is graded **Met / Partial / Not met / Unknown**.

## 2. Project profile

OpenCare-Core's GitHub description is "Empowering Healthy Through Technology in Africa and beyond." The README expands this into "a comprehensive health informatics platform backend built with Django, designed specifically for healthcare management in Africa," organised around Django apps for core functionality, patient management, healthcare-worker administration, facility operations, medical records (with stated FHIR compliance as a goal), and analytics. The presence of `manage.py`, `requirements.txt`, `requirements-dev.txt`, `Dockerfile`, and `docker-compose.yml` indicates a runnable Django scaffold rather than a placeholder.

The project was created on 20 August 2025 and was last pushed on 24 April 2026 — five days before the snapshot — so it is **actively developed**. GitHub-side metrics: **38 forks, 1 star, 66 open issues, ~35 open and ~19 closed pull requests**. The forks-to-stars ratio (38:1) again signals contributor-driven engagement, consistent with a coursework cohort.

## 3. Licensing

OpenCare-Core ships an `MIT License` at the repository root. MIT is OSI-approved and matches the rest of the BOSC organisation. **Principle 1: Met.**

## 4. Governance and community files

The repository root contains, among other files: `LICENSE`, `CONTRIBUTING.md`, `Dockerfile`, `README.md`, `Sample.py`, `manage.py`, `requirements.txt`, `requirements-dev.txt`, `docker-compose.yml`, plus the `apps/`, `config/`, `docs/`, `scripts/`, and `templates/` directories. Notably, **`CONTRIBUTING.md` is present** — OpenCare-Core is the **only one of the four flagship BOSC repositories** that ships a committed contributor guide at the repository root.

What is still missing is `CODE_OF_CONDUCT.md` and `SECURITY.md`. The latter is a meaningful gap for a healthcare-informatics project: the README explicitly mentions FHIR compliance and the system handles patient records, so a documented vulnerability-disclosure pathway has a clear use case. As with the other BOSC projects, the BOSC-wide governance documents (`CONSTITUTION.md`, `GOVERNANCE.md`, `CODE_OF_CONDUCT.md`) live in `bos-com/bosc-governance` but are not linked from this project's README.

**Principle 3: Partial** — better than the other three flagship projects, but still not complete at the repository level. **Principle 6: Not met.**

## 5. Contribution workflow

OpenCare-Core has the **highest aggregate PR volume** of the four projects: roughly **54 total PRs (35 open, 19 closed)**. Activity is recent — the most recent push was 24 April 2026 — and PRs continue to be opened in late April. The open-to-closed ratio of ~1.8:1 indicates that submission velocity is outpacing review velocity. That is a workable position for now, but it is the kind of ratio that becomes a problem if it continues to widen: contributors who wait too long for feedback typically disengage.

As with GreenCode, public issue and PR views show no visible labels, milestones, "good first issue" tags, or assignees. Adding even a minimal triage layer would help contributors self-select work and would help reviewers prioritise.

**Principle 2: Met.** The README is detailed and developer-facing: it identifies the framework, the apps, the deployment story, and the FHIR aspiration. **Principle 4: Partial** — `CONTRIBUTING.md` is a real strength, but triage hygiene is thin. **Principle 5: Met** — last push five days before snapshot, sustained PR activity.

## 6. Verdict and recommendations

| Principle | Verdict |
|---|---|
| 1. Recognised licence at root | **Met** (MIT) |
| 2. README covers purpose, scope, setup | **Met** |
| 3. Explicit project-level governance | **Partial** (CONTRIBUTING.md present, others absent) |
| 4. Inclusive contribution workflow | **Partial** |
| 5. Active maintenance and review velocity | **Met** |
| 6. Code of conduct + security policy | **Not met** |

**Three concrete next actions, in priority order:**

1. **Add a `SECURITY.md`.** Of the four BOSC flagship projects, OpenCare-Core has the strongest case for a documented disclosure pathway — patient records and FHIR compliance imply that vulnerabilities here matter beyond developer convenience. A short policy with a contact address and a response-time target is enough.
2. **Address the open-to-closed PR ratio.** ~1.8:1 is not yet alarming, but it is the leading indicator. A weekly review rhythm — even informal — would close the gap before it widens. Pairing this with a minimal label set (`bug`, `documentation`, `good first issue`, `enhancement`) lets new contributors self-serve.
3. **Link `bos-com/bosc-governance` from the README.** Discoverability of the constitution, governance, and code-of-conduct documents is a one-line fix that lifts this project (and every BOSC project) from "not met" to "partial" on the governance principle.

OpenCare-Core is structurally the **most mature** of the four flagship BOSC projects: it has a runnable Django application, an explicit contributor guide, an OSI-approved licence, and active development on a serious mission. The governance gaps that remain are mostly clerical rather than architectural — closing them is straightforward administrative work.

## 7. Sources

- GitHub REST API: `/repos/bos-com/OpenCare-Core`, `/repos/bos-com/OpenCare-Core/contents/`.
- GitHub web pages: `README.md`, `LICENSE`, `CONTRIBUTING.md`, `/issues`, `/pulls`.
- BOSC governance: `https://github.com/bos-com/bosc-governance`.
- Framework: OSI *Open Source Definition*; GitHub *Open Source Guides*; CHAOSS community-health metrics.

Counts and timestamps are accurate as of 29 April 2026 and will drift as the project develops.
