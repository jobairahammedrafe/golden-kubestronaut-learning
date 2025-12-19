# Contributing to Golden Kubestronaut Learning Path

Thank you for your interest in contributing! This guide helps you get started with contributing to this learning resource.

## Table of Contents

- [How to Contribute](#how-to-contribute)
- [Types of Contributions](#types-of-contributions)
- [Development Setup](#development-setup)
- [Content Guidelines](#content-guidelines)
- [Submitting Changes](#submitting-changes)
- [Style Guide](#style-guide)

## How to Contribute

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/golden-kubestronaut-learning.git
   cd golden-kubestronaut-learning
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and commit them
5. **Push to your fork** and submit a Pull Request

## Types of Contributions

We welcome various types of contributions:

### Study Resources

- Add new study guides for certifications
- Share helpful links and tutorials
- Create cheatsheets and quick references

### Exam Tips

- Share your exam experience (without violating NDA)
- Add general tips and strategies
- Contribute time management advice

### Practice Labs

- Create hands-on lab exercises
- Add Kubernetes manifests for practice
- Develop troubleshooting scenarios

### Documentation

- Fix typos and improve clarity
- Add missing information
- Translate content to other languages

### Flashcards

- Add new flashcard sets for certifications
- Improve existing flashcard content
- Create topic-specific card decks

## Development Setup

### Prerequisites

- Python 3.8+ (for MkDocs)
- Git

### Local Development

```bash
# Install MkDocs and dependencies
pip install mkdocs mkdocs-material

# Serve locally with live reload
mkdocs serve

# Build static site
mkdocs build
```

The site will be available at `http://localhost:8000`.

### Project Structure

```text
golden-kubestronaut-learning/
├── docs/                    # MkDocs documentation source
├── cka/                     # CKA certification resources
├── ckad/                    # CKAD certification resources
├── cks/                     # CKS certification resources
├── kcna/                    # KCNA certification resources
├── kcsa/                    # KCSA certification resources
├── pca/                     # PCA certification resources
├── labs/                    # Hands-on lab exercises
├── cheatsheets/             # Quick reference guides
├── flashcards/              # Study flashcards
├── templates/               # Reusable templates
├── troubleshooting/         # Troubleshooting guides
├── mkdocs.yml               # MkDocs configuration
└── README.md
```

## Content Guidelines

### Certification Content

When adding certification-specific content:

1. **Respect NDAs** - Never share actual exam questions
2. **Focus on concepts** - Explain underlying principles
3. **Provide examples** - Use practical, real-world scenarios
4. **Link official docs** - Reference Kubernetes and CNCF documentation
5. **Keep updated** - Note the certification version/date

### Writing Style

- Use clear, concise language
- Write for beginners but include advanced topics
- Include code examples where applicable
- Add diagrams for complex concepts
- Use bullet points for lists

### File Naming

- Use lowercase with hyphens: `pod-security-policies.md`
- Be descriptive: `network-policies-examples.md` not `np.md`
- Group related files in directories

## Submitting Changes

### Commit Messages

Use conventional commit format:

```text
<type>(<scope>): <description>

[optional body]
```

**Types:**
- `docs`: Documentation changes
- `feat`: New content or features
- `fix`: Corrections or fixes
- `chore`: Maintenance tasks

**Examples:**
```text
docs(cka): add etcd backup and restore guide
feat(labs): add network policy practice lab
fix(ckad): correct deployment rollout command
```

### Pull Request Process

1. **Update documentation** if adding new sections
2. **Test locally** with `mkdocs serve`
3. **Fill out the PR template** completely
4. **Link related issues** if applicable
5. **Request review** from maintainers

### PR Checklist

- [ ] Content follows the style guide
- [ ] No NDA violations
- [ ] Links are working
- [ ] Tested locally with MkDocs
- [ ] Commit messages follow conventions

## Style Guide

### Markdown

- Use ATX-style headers (`#`, `##`, `###`)
- Add blank lines around headers and code blocks
- Use fenced code blocks with language identifiers
- Keep lines under 120 characters when possible

### Code Examples

Always specify the language for syntax highlighting:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: example-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.25
```

### Tables

Use tables for structured information:

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |

### Admonitions

Use MkDocs admonitions for important notes:

```markdown
!!! note
    This is an important note.

!!! warning
    This is a warning message.

!!! tip
    This is a helpful tip.
```

## Questions?

- Open a [Discussion](https://github.com/pmady/golden-kubestronaut-learning/discussions) for questions
- Check existing [Issues](https://github.com/pmady/golden-kubestronaut-learning/issues) for known problems
- Review the [Documentation](https://golden-kubestronaut-learning.readthedocs.io/)

Thank you for helping others on their Kubestronaut journey!
