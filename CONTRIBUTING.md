# Contributing to OpenCare-Core

Thank you for your interest in contributing to OpenCare-Core! We are excited to have you join our community and help improve healthcare systems in Africa.

## 🚀 Getting Started

To contribute to this project, please follow these steps:

### 1. Fork and Clone
Fork the repository on GitHub and clone your fork locally:

```bash
git clone https://github.com/your-username/OpenCare-Core.git
cd OpenCare-Core
```

Add the original repository as a remote named `upstream`:
```bash
git remote add upstream https://github.com/bos-com/OpenCare-Core.git
```

### 2. Branching Strategy
Always create a new branch for your work. We use the following naming convention:

- `feature/your-feature-name` for new features
- `fix/your-fix-name` for bug fixes
- `docs/your-topic` for documentation updates

```bash
git checkout -b feature/amazing-new-feature
```

### 3. Commit Message Style
We follow the **Conventional Commits** specification. This helps us generate automated changelogs.

Format: `<type>(<scope>): <description>`

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries

**Example:** `feat(patients): add ability to search patients by ID`

### 4. Pull Request (PR) Process
When you are ready to submit your changes:

1.  **Push** your branch to your fork:
    ```bash
    git push origin feature/amazing-new-feature
    ```
2.  **Open a PR** on GitHub.
3.  **Description**: In the PR description, explain what you changed and why.
4.  **Link Issues**: If your PR fixes an open issue, link it using keywords like `Closes #123`.
5.  **Review**: A maintainer will review your code. Address any feedback by pushing additional commits to your branch.

---

## 🛠️ Development Setup

For detailed instructions on setting up your local environment, please refer to the [README.md](README.md#🚀-quick-start).

## ⚖️ Code of Conduct
By participating in this project, you agree to abide by our Code of Conduct.

---

**Together, we can build a healthier future for Africa!** 🩺🌍
