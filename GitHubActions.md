# Git Workflow and CI/CD Pipeline Setup

This document details the recommended Git workflow and CI/CD pipeline using GitHub Actions, tailored specifically for our development practices.

## 📌 Git Workflow Overview

### Branching Strategy:

| Branch Type   | Purpose                              | Automation Behavior                              |
| -------------| ------------------------------------- | ------------------------------------------------ |
| `main`       | Production-ready, stable code         | Auto-tags and creates a release on merge         |
| `release/*`  | Release preparation & RC tagging      | Creates Release Candidate (RC) tags              |
| `develop`    | Integration and testing branch        | No RC tags, prepares for release                 |
| `feature/*`  | New feature development               | Auto-merge into `develop` after successful tests |
| `hotfix/*`   | Critical fixes                        | Auto-merge into `develop` after successful tests |

## 🔄 Workflow Steps

### 1. Development Workflow

* Create a new branch from `develop` for features:

  ```bash
  git checkout develop
  git pull
  git checkout -b feature/my-new-feature
  ```
* Push to remote and trigger automated testing:

  ```bash
  git push -u origin feature/my-new-feature
  ```
* GitHub Actions automatically runs tests and merges to `develop` upon success all time time!

### 2. Creating Release Candidates

* When ready for a release, create a `release/x.y.z` branch from `develop` (note the full semantic version):

  ```bash
  git checkout develop
  git pull
  git checkout -b release/1.2.0
  git push -u origin release/1.2.0
  ```
* Pushing to `release/x.y.z` triggers automated tests and semantic-release.
* After successful tests, semantic-release automatically creates RC tags:

  ```
  v1.2.0-rc.1, v1.2.0-rc.2, ...
  ```
* Deploy and test using the RC tag.

### 3. Production Release

* After successful RC testing, manually create a Pull Request (PR) from the `release/x.y.z` branch to `main`.
* Merging PR into `main` automatically triggers a new production release (`v1.2.0`).

## ⚙️ GitHub Actions Workflows

### `.github/workflows/ci.yml`

```yaml
name: CI for PyEasyCmdLine

on:
  push:
    branches:
      - "feature/*"
      - "hotfix/*"
      - develop
      - main
  pull_request:
    branches:
      - develop
      - main

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: make dev-install

      - name: Lint code
        run: make lint

      - name: Run tests
        run: make test

      - name: Generate coverage report
        run: make coverage

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/

  auto-merge-to-develop:
    if: github.event_name == 'push' && (startsWith(github.ref, 'refs/heads/feature/') || startsWith(github.ref, 'refs/heads/hotfix/'))
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: develop
          fetch-depth: 0

      - name: Merge branch into develop
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git merge --no-ff origin/${{ github.ref_name }}
          git push origin develop
```

### `.github/workflows/release.yml`

```yaml
name: Release Workflow

on:
  push:
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

      - run: make dev-install
      - run: make lint
      - run: make test
      - run: make coverage

  create-rc-tag:
    if: github.ref == 'refs/heads/release/*'
    needs: tests-and-coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: develop

      - name: Create RC Tag
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          LAST_TAG=$(git tag -l 'v*-rc.*' --sort=-v:refname | head -n1)
          if [[ -z "$LAST_TAG" ]]; then
              NEW_TAG="v0.1.0-rc.1"
          else
              BASE_VERSION=$(echo $LAST_TAG | sed 's/-rc.*//')
              RC_NUMBER=$(echo $LAST_TAG | grep -oE '[0-9]+$')
              NEW_RC_NUMBER=$((RC_NUMBER+1))
              NEW_TAG="$BASE_VERSION-rc.$NEW_RC_NUMBER"
          fi

          git tag -a $NEW_TAG -m "Auto RC tag $NEW_TAG"
          git push origin $NEW_TAG

  release-on-main:
    if: github.ref == 'refs/heads/main'
    needs: tests-and-coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: main

      - name: Create Production Release Tag
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          LAST_RC=$(git tag -l 'v*-rc.*' --sort=-v:refname | head -n1)
          RELEASE_VERSION=$(echo $LAST_RC | sed 's/-rc.*//')

          git tag -a $RELEASE_VERSION -m "Production Release $RELEASE_VERSION"
          git push origin $RELEASE_VERSION

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: $RELEASE_VERSION
          generate_release_notes: true
```

## 🚧 Branch Protection

Ensure `main` and `develop` branches are protected with rules to allow only merges from GitHub Actions or PRs.

---

This comprehensive workflow ensures quality, traceability, and efficiency across our development lifecycle.

