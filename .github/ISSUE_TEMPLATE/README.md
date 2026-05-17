# Issue Templates Guide

Welcome to OpenCare-Core! This guide explains our issue system to help you choose the right template and understand how we triage and manage issues.

---

## 📋 Which Template Should I Use?

### Bug Reports 🐛
Use **Bug Report** when:
- You found something that isn't working as expected
- There's an error or unexpected behavior
- A feature is producing incorrect results

**What to include:** Steps to reproduce, expected vs. actual behavior, logs, and environment details.

---

### Feature Requests ✨
Use **Feature Request** when:
- You have an idea for a new feature
- You want to enhance existing functionality
- You've identified an unmet user need

**What to include:** The problem it solves, your proposed solution, and alternative approaches you've considered.

---

### Security Issues 🔒
Use **Security Issue** when:
- You've found a potential security vulnerability
- There's a risk to data privacy or system integrity

⚠️ **Important:** Do NOT include secrets, credentials, or exploit code. For sensitive vulnerabilities, use our [Security Policy](https://github.com/bos-com/OpenCare-Core/security/policy) instead.

---

## 🎯 Difficulty Levels

Issues are categorized by difficulty to help contributors find tasks matching their experience level.

### 🟢 Beginner Issues
**Who:** New contributors with limited codebase knowledge

**Characteristics:**
- Small and well-scoped
- Single file or minimal changes
- No deep architecture knowledge required
- Clear expected outcomes
- Great for learning the codebase

**Duration:** A few hours to a day

---

### 🟡 Intermediate Issues
**Who:** Contributors familiar with the codebase and Django patterns

**Characteristics:**
- May touch multiple files or modules
- Requires understanding existing patterns
- May involve testing or refactoring
- Clearly bounded but meaningful effort

**Duration:** A few days

---

### 🔴 Advanced Issues
**Who:** Experienced contributors or maintainers

**Characteristics:**
- Architectural decisions or major refactoring
- Security or performance implications
- Affects multiple systems
- Complex design considerations

**Duration:** Weeks or ongoing work

---

### 🎯 Good First Issue vs. Good First Issue Candidate

#### **Good First Issue** (`good first issue`)
- Maintainers have reviewed and refined the issue
- Verified to be suitable for newcomers
- Clear context, acceptance criteria, and resources
- Ready for contribution

#### **Good First Issue Candidate** (`good-first-issue-candidate`)
- Proposed as a potential good first issue
- Requires maintainer refinement before final labeling
- May need clarification or additional context
- Review process: Candidate → Refined → `good first issue` label applied

---

## 🏷️ Label System

We use labels to categorize and organize issues:

| Label | Meaning |
|-------|---------|
| `bug` | Something isn't working |
| `enhancement` | Feature request or improvement |
| `security` | Security vulnerability or concern |
| `beginner` | Suitable for new contributors |
| `intermediate` | Requires codebase familiarity |
| `advanced` | Complex, architectural work |
| `good first issue` | Verified entry point for newcomers |
| `good-first-issue-candidate` | Potential good first issue, under review |

---

## 🔄 Maintainer Triage & Workflow

When maintainers review issues, they:

1. **Verify** the issue is clear and reproducible (for bugs)
2. **Assess** scope and complexity
3. **Apply** difficulty labels (`beginner`, `intermediate`, `advanced`)
4. **Consider** if it's a good first issue candidate
5. **Label accordingly:**
   - `good first issue` → Ready for new contributors
   - `good-first-issue-candidate` → Needs refinement first

---

## 💡 Tips for Issue Authors

✅ **Do:**
- Search existing issues first to avoid duplicates
- Provide clear, specific details
- Include steps to reproduce (for bugs)
- Link related issues or discussions
- Be respectful and constructive

❌ **Don't:**
- Use multiple issue types in one report
- Include secrets, credentials, or sensitive data
- Ask for feature requests in bug reports
- Submit vague or overly broad issues

---

## 📞 Getting Help

- **Questions about contributing?** → Open an issue or start a discussion
- **Found a security vulnerability?** → Report via [Security Policy](https://github.com/bos-com/OpenCare-Core/security/policy)
- **Need clarification on an issue?** → Comment on the issue

---

## 🙏 Thank You

We appreciate your contributions to OpenCare-Core! Following these guidelines helps us maintain a healthy, welcoming community.
