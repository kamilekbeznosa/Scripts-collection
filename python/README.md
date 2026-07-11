# Python DevOps Automation Toolkit

[![Python CI](https://github.com/kamilekbeznosa/Scripts-collection/actions/workflows/python-ci.yml/badge.svg)](https://github.com/kamilekbeznosa/Scripts-collection/actions/workflows/python-ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Coverage](https://img.shields.io/badge/Coverage-%E2%89%A540%25-yellowgreen)

Production-style CLI tools for day-to-day DevOps operations — Azure cost reporting, GitHub repository compliance audits, Kubernetes health checks, and TLS certificate monitoring.

This is **not a collection of loose scripts**. It is a packaged toolkit with a `src/` layout, separated CLI and service layers, unit tests with API mocking, linting, and a GitHub Actions pipeline.

Part of the [Scripts-collection](https://github.com/kamilekbeznosa/Scripts-collection) portfolio alongside Bash and PowerShell utilities.

---

## Table of Contents

- [Tools](#tools)
- [Architecture](#architecture)
- [Engineering Standards](#engineering-standards)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Testing & CI/CD](#testing--cicd)
- [Skills Demonstrated](#skills-demonstrated)

---

## Tools

| CLI command | Description | Technologies |
|---|---|---|
| `azure-cost-reporter` | Fetches Azure subscription costs for the last 30 days (grouped by Resource Group) and posts a report to a webhook. Supports `--dry-run` with mock data. | `azure-identity`, `azure-mgmt-costmanagement` |
| `github-repo-auditor` | Audits GitHub user/org repositories for policy violations (missing description, disabled Issues). Handles API pagination and rate limits. | `requests`, GitHub REST API, `tenacity` |
| `k8s-health-checker` | Scans a Kubernetes namespace for operational issues: failed pods, `CrashLoopBackOff`, `ImagePullBackOff`. | `kubernetes` Python client |
| `dns-cert-monitor` | Checks SSL/TLS certificate expiry for multiple domains defined in a YAML config file. | `ssl`, `socket`, `PyYAML` |

---

## Architecture

```text
python/
├── config/
│   ├── example.yaml          # committed template (no secrets)
│   └── local.yaml            # your overrides (gitignored)
├── src/devops_toolkit/
│   ├── commands/             # Typer CLI — argument parsing only
│   └── services/             # business logic — tested with pytest
└── tests/                    # unit tests with mocked API responses
```

**Separation of concerns:** `commands/` parse CLI flags and call `services/`. All testable logic lives in `services/` — no subprocess spawning in tests.

Each tool is registered as an entry point in `pyproject.toml` and becomes globally available after `pip install -e .`.

---

## Engineering Standards

| Standard | Implementation |
|---|---|
| **CLI framework** | [Typer](https://typer.tiangolo.com/) with `--help`, `--verbose`, `--json` |
| **Retries** | `tenacity` with exponential backoff on GitHub API calls |
| **Rate limiting** | GitHub: waits for `X-RateLimit-Reset` when quota is exhausted |
| **Secrets** | Environment variables only — never flags, never committed YAML |
| **Logging** | Structured `logging` module — no `print()` in services |
| **Exit codes** | POSIX-compatible for CI/CD pipelines (see below) |
| **Testing** | `pytest` + `unittest.mock` / `responses`, coverage gate in CI |
| **Linting** | `ruff check` + `ruff format --check` in GitHub Actions |

### Exit codes

Designed for automation (`set -e`, `if command; then ...`):

| Code | Meaning |
|---|---|
| `0` | Success — no issues found |
| `1` | Operational issues detected (audit failures, expiring certs, unhealthy pods) |
| `2` | Configuration error (missing env var, invalid/missing YAML) |
| `3` | External API unreachable (e.g. webhook POST failed) |

---

## Installation

```bash
git clone https://github.com/kamilekbeznosa/Scripts-collection.git
cd Scripts-collection/python

# Editable install with dev dependencies (pytest, ruff, coverage)
pip install -e ".[dev]"
```

Verify installation:

```bash
azure-cost-reporter --help
github-repo-auditor --help
k8s-health-checker --help
dns-cert-monitor --help
```

---

## Configuration

### Environment variables

| Variable | Required by | Description |
|---|---|---|
| `GITHUB_TOKEN` | `github-repo-auditor` | GitHub PAT with `repo` or `read:org` scope |
| `AZURE_SUBSCRIPTION_ID` | `azure-cost-reporter` | Target Azure subscription GUID |
| `WEBHOOK_URL` | `azure-cost-reporter` | Webhook endpoint (Discord, Teams, Slack, webhook.site) |
| `USE_MOCK_DATA` | `azure-cost-reporter` | Set to `true` to force mock cost data without Azure API calls |
| `KUBECONFIG` | `k8s-health-checker` | Defaults to `~/.kube/config`; in-cluster SA also supported |

**Example (PowerShell):**

```powershell
$env:GITHUB_TOKEN = "ghp_xxxxxxxx"
$env:AZURE_SUBSCRIPTION_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
$env:WEBHOOK_URL = "https://webhook.site/your-unique-id"
```

**Example (Bash):**

```bash
export GITHUB_TOKEN="ghp_xxxxxxxx"
export AZURE_SUBSCRIPTION_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export WEBHOOK_URL="https://webhook.site/your-unique-id"
```

### YAML config (dns-cert-monitor)

Copy the example and add your domains:

```bash
cp config/example.yaml config/local.yaml
```

```yaml
# config/local.yaml
logging:
  level: INFO

dns_monitor:
  warn_days: 14
  domains:
    - github.com
    - your-domain.com
```

> `config/local.yaml` is gitignored. Only commit `config/example.yaml`.

---

## Usage Examples

### 1. Kubernetes Health Checker

Quick cluster diagnostics — detects pods in critical states.

```bash
# Human-readable output
k8s-health-checker check --namespace default

# Machine-readable output for CI pipelines
k8s-health-checker check -n kube-system --json
```

**Requires:** valid kubeconfig pointing at a reachable cluster (local k3d/kind, AKS, or any K8s).

---

### 2. Azure Cost Reporter

Generates a cost report and optionally sends it to a webhook.

```bash
# Dry run — mock data, no Azure API call, no webhook POST
azure-cost-reporter report --dry-run

# JSON output
azure-cost-reporter report --dry-run --json

# Live report — requires az login (DefaultAzureCredential) + env vars
azure-cost-reporter report

# Explicit flags instead of env vars
azure-cost-reporter report \
  --subscription-id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
  --webhook "https://webhook.site/your-id" \
  --dry-run
```

**Auth:** uses `DefaultAzureCredential()` — works with `az login` locally or service principal env vars in CI.

---

### 3. GitHub Repository Auditor

Scans repositories for compliance violations.

**Current checks:**
- Missing repository `description`
- Disabled Issues (`has_issues: false`)

```bash
# Audit a user account
github-repo-auditor audit kamilekbeznosa

# Audit an organization
github-repo-auditor audit my-org --org

# Debug logging + JSON output
github-repo-auditor audit kamilekbeznosa --verbose --json
```

Exit code `1` if any repository fails the audit — ready for use in CI gates.

---

### 4. DNS / SSL Certificate Monitor

Checks certificate expiry for all domains in the YAML config.

```bash
# Default config (config/example.yaml)
dns-cert-monitor check

# Custom config file
dns-cert-monitor check --config config/local.yaml

# Verbose + JSON
dns-cert-monitor check -c config/local.yaml --verbose --json
```

Exit code `1` if any certificate expires within `warn_days`.

---

## Testing & CI/CD

Run the full test suite locally:

```bash
cd python

# Tests with coverage report
pytest --cov=src/devops_toolkit/services --cov-report=term-missing

# Lint and format check
ruff check .
ruff format --check .
```

**CI pipeline** (`.github/workflows/python-ci.yml`) runs on every push/PR touching `python/`:

1. `ruff check` + `ruff format --check`
2. `pytest` with coverage gate (≥ 40%)

Dummy env vars are injected in CI so tests never hit real APIs.

---

## Skills Demonstrated

Portfolio / CV bullet points (add after linking this repo):

- Developed a **Python automation toolkit** (Azure SDK, GitHub REST API, Kubernetes client) for cost reporting, repository compliance audits, cluster health checks, and certificate monitoring — with **retry logic**, structured logging, and **YAML configuration**.
- Applied production engineering practices: **`src/` layout**, Typer CLI, **pytest** with API mocking, **ruff** linting, and **GitHub Actions CI** with coverage gates.

**Technologies:** Python, Typer, Azure SDK, GitHub API, Kubernetes, pytest, ruff, tenacity, PyYAML, GitHub Actions

---

## Related Projects

| Project | Connection |
|---|---|
| [Observability Platform](../) (Project 1) | `k8s-health-checker` scans the same clusters monitored by Prometheus/Grafana |
| `bash/ssl_expiry_checker.sh` | Superseded by `dns-cert-monitor` with multi-domain YAML, retries, and exit codes |
| Azure DevOps CI/CD project | `ado-pipeline-monitor` (planned stretch tool) will audit pipeline runs |

---

## License

MIT — same as the parent repository.
