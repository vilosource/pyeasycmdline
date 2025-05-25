# GitHub Workflow How-To: Semver-Compliant Python Release Automation

This document provides all the context and rationale needed for an AI to generate robust, semver-compliant GitHub Actions workflows for Python projects using Poetry and python-semantic-release, following a develop/release/main branching model.

---

## Branching Model

- **main**: Production-ready, stable code. Only stable releases are published from here.
- **develop**: Integration and testing branch. All features and hotfixes are merged here first.
- **release/x.y.z**: Release preparation branches. Used for release candidate (RC) tagging and pre-release testing.
- **feature/** and **hotfix/**: Short-lived branches for new features and critical fixes, respectively. Auto-merged into `develop` after successful CI.

## Release Workflow

1. **Feature/Hotfix Development**
   - Branch from `develop` (e.g., `feature/my-feature` or `hotfix/urgent-fix`).
   - Push triggers CI (tests, lint, coverage).
   - On success, auto-merge into `develop`.

2. **Release Candidate Creation**
   - When ready, create a branch from `develop` named `release/x.y.z` (full semantic version, e.g., `release/1.2.0`).
   - Push triggers CI and semantic-release.
   - On success, semantic-release creates RC tags: `v1.2.0-rc.1`, `v1.2.0-rc.2`, etc.
   - RC tags are used for pre-release testing and deployment.

3. **Production Release**
   - After RC testing, create a PR from `release/x.y.z` to `main`.
   - Merging triggers a stable release (`v1.2.0`) and PyPI publish.

## Required Files and Configuration

### 1. `.github/workflows/ci.yml`
- Runs on pushes to `feature/*`, `hotfix/*`, `develop`, and `main`.
- Runs tests, lint, and coverage.
- Auto-merges feature/hotfix branches into `develop` after successful CI.

### 2. `.github/workflows/release.yml`
- Runs on pushes to `release/**` and `main`.
- Runs tests, lint, and coverage.
- Runs `poetry run semantic-release publish` to create tags and releases.
- Only publishes to PyPI on `main`.

#### Example Trigger:
```yaml
on:
  push:
    branches:
      - "release/**"
      - main
```

### 3. `.releaserc`
- Configures semantic-release for Python/Poetry.
- Branches:
  - `main`: stable releases
  - `release/**`: pre-releases with `rc` suffix
- Tag format: `v${version}`
- Ensures version is read from and written to code (see `pyproject.toml` below).

#### Example:
```json
{
  "branches": [
    "main",
    { "name": "release/**", "prerelease": "rc" }
  ],
  "tagFormat": "v${version}",
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/github",
    "@semantic-release/git",
    ["@semantic-release/exec", {
      "publishCmd": "poetry publish --build --no-interaction"
    }]
  ]
}
```

### 4. `pyproject.toml`
- Add `python-semantic-release` as a dev dependency.
- Add a `[tool.semantic_release]` section with `version_variable` pointing to the code (e.g., `easycmdline/__init__.py:__version__`).

#### Example:
```toml
[tool.semantic_release]
version_variable = "easycmdline/__init__.py:__version__"
```

### 5. Version Variable in Code
- Ensure your package's `__init__.py` contains a line like:
  ```python
  __version__ = "0.1.0"
  ```

## Best Practices
- Protect `main` and `develop` branches to allow only merges from PRs or GitHub Actions.
- Use full semantic versioning in release branch names (e.g., `release/1.2.0`).
- Only publish to PyPI from `main`.
- Use semantic-release for all versioning and tagging; do not create tags manually.

## Summary Table
| Branch Type   | Purpose                              | Automation Behavior                              |
| -------------| ------------------------------------- | ------------------------------------------------ |
| `main`       | Production-ready, stable code         | Auto-tags and creates a release on merge         |
| `release/**` | Release preparation & RC tagging      | Creates Release Candidate (RC) tags              |
| `develop`    | Integration and testing branch        | No RC tags, prepares for release                 |
| `feature/*`  | New feature development               | Auto-merge into `develop` after successful tests |
| `hotfix/*`   | Critical fixes                        | Auto-merge into `develop` after successful tests |

---

This document is sufficient for an AI to generate the correct workflow and configuration files for any similar Python project using Poetry and semantic-release.
