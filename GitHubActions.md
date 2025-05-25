# Git Workflow and CI/CD Pipeline Setup

This document details the Git workflow and CI/CD pipeline using GitHub Actions with **python-semantic-release** for automated versioning and releases.

## 📌 Git Workflow Overview

### Branching Strategy with Semantic Release:

| Branch Type   | Purpose                              | Semantic Release Behavior                         |
| -------------| ------------------------------------- | ------------------------------------------------ |
| `main`       | Production-ready, stable code         | Creates **production releases** (e.g., `v0.2.1`) |
| `release/*`  | Release preparation & RC testing      | Creates **release candidates** (e.g., `v0.2.1-rc.1`) |
| `develop`    | Integration and testing branch        | No automatic releases                            |
| `feature/*`  | New feature development               | No automatic releases                            |
| `hotfix/*`   | Critical fixes                        | No automatic releases                            |

### 🎯 Semantic Commit Messages

For semantic-release to work properly, use conventional commit messages:

```bash
feat: add new command validation feature    # → MINOR version bump
fix: resolve configuration loading bug      # → PATCH version bump  
docs: update API documentation             # → No version bump
BREAKING CHANGE: change CLI interface      # → MAJOR version bump
``` 

## 🔄 Workflow Steps

### 1. Development Workflow

**Feature Development:**
```bash
git checkout develop
git pull
git checkout -b feature/my-new-feature
# Make changes with semantic commits
git commit -m "feat: add new command validation"
git push -u origin feature/my-new-feature
```

**Merge to develop:** Create PR → Review → Merge (no releases triggered)

### 2. Release Candidate Creation

**Create Release Branch:**
```bash
git checkout develop
git pull
git checkout -b release/0.2.0  # Use target version
git push -u origin release/0.2.0
```

**What happens automatically:**
1. 🚀 GitHub Actions triggers the **release workflow**
2. 🧪 Runs all tests and quality checks
3. 🏷️ **python-semantic-release** analyzes commit history since last release
4. 📦 Creates **Release Candidate** version (e.g., `v0.2.1-rc.1`)
5. 🔨 Builds Python packages (`wheel` and `tar.gz`)
6. 📋 Generates changelog from commit messages
7. 🏷️ Creates Git tag and pushes to repository
8. 📱 Creates GitHub Release (marked as pre-release)

**Example RC versions:**
- First RC: `v0.2.1-rc.1`
- Second RC: `v0.2.1-rc.2` (if you push more commits)
- Third RC: `v0.2.1-rc.3` (and so on...)

### 3. Testing Release Candidates

```bash
# Install and test the RC
pip install https://github.com/vilosource/pyeasycmdline/releases/download/v0.2.1-rc.1/pyeasycmdline-0.2.1rc1-py3-none-any.whl

# Or test from PyPI (if published there)
pip install pyeasycmdline==0.2.1rc1
```

### 4. Production Release (Merge to Main)

**When you're satisfied with the RC:**

1. **Create Pull Request:** `release/0.2.0` → `main`
2. **Review and approve the PR**
3. **Merge to main**

**What happens when merging to main:**
1. 🚀 GitHub Actions triggers the **release workflow** on `main` branch
2. 🧪 Runs all tests and quality checks  
3. 🏷️ **python-semantic-release** creates **production release** (e.g., `v0.2.1`)
4. 📦 Builds final Python packages
5. 📋 Updates changelog
6. 🏷️ Creates production Git tag
7. 📱 Creates **official GitHub Release** (not pre-release)
8. 🐍 **Publishes to PyPI** (if `PYPI_TOKEN` is configured)

**Version progression example:**
```
v0.2.0 (last production) → v0.2.1-rc.1 (RC) → v0.2.1 (production)
```

## ⚙️ GitHub Actions Workflows

### `.github/workflows/ci.yml` - Continuous Integration

Runs on every push to feature branches and PRs:

```yaml
name: CI for PyEasyCmdLine

on:
  push:
    branches:
      - "feature/*"
      - "hotfix/*"
      - develop
  pull_request:
    branches:
      - develop
      - main

jobs:
  tests-and-coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        uses: snok/install-poetry@v1

      - name: Install dependencies
        run: make dev-install

      - name: Lint code
        run: make lint

      - name: Run tests with coverage
        run: make test

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/
```

### `.github/workflows/release.yml` - Semantic Release

Runs on pushes to `release/*` branches and `main`:

```yaml
name: Release Workflow

on:
  push:
    branches:
      - main
      - "release/*"

jobs:
  tests-and-coverage:
    # ... same as CI workflow ...

  semantic-release:
    needs: tests-and-coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for semantic-release

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        uses: snok/install-poetry@v1

      - name: Install dependencies
        run: make dev-install

      - name: Run Semantic Release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          poetry run semantic-release publish

      - name: Publish to PyPI (main branch only)
        if: github.ref == 'refs/heads/main'
        env:
          POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_TOKEN }}
        run: |
          poetry publish --build --no-interaction
```

## 🔧 Semantic Release Configuration

The semantic release behavior is configured in `pyproject.toml`:

```toml
[tool.semantic_release]
version_variables = ["easycmdline/__init__.py:__version__"]
version_toml = ["pyproject.toml:tool.poetry.version"]
upload_to_vcs_release = true
build_command = "poetry build"
major_on_zero = false
tag_format = "v{version}"

# Main branch: creates production releases
[tool.semantic_release.branches.main]
match = "main"
prerelease = false

# Release branches: creates release candidates  
[tool.semantic_release.branches.release]
match = "release/.*"
prerelease = true
prerelease_token = "rc"
```

## 🎯 Key Points

### ✅ **Do I need to merge to main after RC testing?**

**YES!** Here's the flow:

1. **Release branch** (`release/0.2.0`) → Creates **RC versions** (`v0.2.1-rc.1`, `v0.2.1-rc.2`, etc.)
2. **Test the RC thoroughly** 
3. **Create PR:** `release/0.2.0` → `main` 
4. **Merge to main** → Creates **production release** (`v0.2.1`)

### 🚀 **What happens when merging to main?**

1. **Triggers release workflow** on `main` branch
2. **Semantic-release analyzes commits** since last production release
3. **Creates production version** (strips `-rc.X` suffix)
4. **Updates version files** (`__init__.py`, `pyproject.toml`)
5. **Builds final packages**
6. **Creates production Git tag** (e.g., `v0.2.1`)
7. **Creates GitHub Release** (official, not pre-release)
8. **Publishes to PyPI** (if token configured)

### 📋 **Version Timeline Example:**

```
develop branch:
├─ feat: add validation (commit)
├─ fix: bug in parser (commit) 
└─ release/0.2.0 branch created
   │
   ├─ Push → v0.2.1-rc.1 (first RC)
   ├─ fix: RC bug → v0.2.1-rc.2 (second RC)  
   └─ Merge to main → v0.2.1 (production)
```

### 🔒 **Important Notes:**

- **Only `fix:`, `feat:`, `BREAKING CHANGE:` commits trigger versions**
- **RC versions are for testing only** - not production
- **Production releases only happen on `main` branch**
- **PyPI publishing only happens on `main` branch**
- **Always test RCs before merging to main**

## 🚨 Hotfix Workflow (Bug in Production)

**Scenario:** You've released `v0.2.1` to production and discovered a critical bug that needs immediate fixing.

### Option 1: Direct Hotfix to Main (Fastest)

**For critical bugs that need immediate production deployment:**

```bash
# 1. Create hotfix branch from main (current production)
git checkout main
git pull
git checkout -b hotfix/fix-critical-bug

# 2. Fix the bug with semantic commit
git commit -m "fix: resolve critical parsing error in CLI"

# 3. Push hotfix branch
git push -u origin hotfix/fix-critical-bug

# 4. Create PR: hotfix/fix-critical-bug → main
# 5. Review and merge to main
```

**What happens when merging to main:**
1. 🚀 **Triggers release workflow** on `main` branch
2. 🏷️ **Creates patch release** `v0.2.2` (since it's a `fix:` commit)
3. 📦 **Builds and publishes** to PyPI immediately
4. 📱 **Creates GitHub Release** with the bug fix

### Option 2: Hotfix via Release Branch (More Testing)

**For bugs that need testing before production:**

```bash
# 1. Create hotfix branch from main
git checkout main
git pull
git checkout -b hotfix/fix-critical-bug

# 2. Fix the bug
git commit -m "fix: resolve critical parsing error in CLI"

# 3. Create release branch for testing
git checkout -b release/0.2.2
git push -u origin release/0.2.2
```

**Release branch workflow:**
1. ⚡ **Creates RC:** `v0.2.2-rc.1`
2. 🧪 **Test the hotfix RC thoroughly**
3. 📋 **Create PR:** `release/0.2.2` → `main`
4. ✅ **Merge to main** → Creates `v0.2.2` production release

### 🎯 **Which Option to Choose?**

| Scenario | Recommended Approach | Reason |
|----------|---------------------|---------|
| **Critical security bug** | Option 1 (Direct to main) | Fastest deployment |
| **Data corruption bug** | Option 1 (Direct to main) | Immediate fix needed |
| **Complex logic bug** | Option 2 (Release branch) | Needs thorough testing |
| **UI/UX bug** | Option 2 (Release branch) | Can afford testing time |

### 📋 **Hotfix Version Timeline Example:**

```
v0.2.1 (production with bug)
└─ hotfix/fix-critical-bug
   ├─ Option 1: Direct merge → v0.2.2 (immediate)
   └─ Option 2: release/0.2.2 → v0.2.2-rc.1 → test → merge → v0.2.2
```

### 🔄 **After Hotfix: Sync Back to Develop**

**Important:** Always sync the hotfix back to develop to prevent regression:

```bash
# After hotfix is merged to main
git checkout develop
git pull
git merge main  # Brings the hotfix into develop
git push
```

### 🚀 **Emergency Rollback (if needed)**

If the hotfix causes more issues:

```bash
# 1. Revert the problematic commit on main
git checkout main
git revert <commit-hash>
git commit -m "fix: revert problematic hotfix"
git push

# 2. This creates another patch version (e.g., v0.2.3)
# 3. Work on proper fix in a new branch
```

## 🚧 Branch Protection

Set up branch protection rules in GitHub:

- **Protect `main` branch:** Require PR reviews, require status checks
- **Protect `develop` branch:** Require PR reviews for direct pushes
- **Allow GitHub Actions** to push to both branches for automation

---

*This workflow ensures automated, reliable releases with proper testing at every stage.*
