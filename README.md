# Scripts-collection

[![Python CI](https://github.com/kamilekbeznosa/Scripts-collection/actions/workflows/python-ci.yml/badge.svg)](https://github.com/kamilekbeznosa/Scripts-collection/actions/workflows/python-ci.yml)

A curated collection of operational scripts and CLI tools for DevOps automation — organized by language and built to demonstrate real-world platform engineering practices.

This repository grew from learning Bash and PowerShell scripting into a **production-style Python toolkit** with tests, linting, and CI/CD. It is part of my DevOps portfolio alongside [IaacProjects](https://github.com/kamilekbeznosa/IaacProjects) (Terraform/Azure) and the Kubernetes Observability GitOps platform.

---

## Repository Structure

```text
Scripts-collection/
├── bash/           # Shell scripts for Linux/macOS/WSL automation
├── Powershell/     # PowerShell scripts for Windows / Azure admin tasks
├── python/         # Packaged CLI toolkit (Typer, pytest, CI)  ← main portfolio piece
└── .github/
    └── workflows/
        └── python-ci.yml
```

---

## Python Automation Toolkit

**Location:** [`python/`](python/)

The flagship of this repository — four CLI tools for Azure, GitHub, Kubernetes, and TLS monitoring. Built with a `src/` layout, separated command/service layers, mocked unit tests, and a GitHub Actions pipeline.

| Tool | One-liner |
|---|---|
| `azure-cost-reporter` | Azure cost report → webhook (with `--dry-run`) |
| `github-repo-auditor` | GitHub repo compliance scan with pagination & rate-limit handling |
| `k8s-health-checker` | Kubernetes namespace health check (CrashLoopBackOff, Failed pods) |
| `dns-cert-monitor` | Multi-domain SSL/TLS expiry monitor via YAML config |

```bash
cd python
pip install -e ".[dev]"

github-repo-auditor audit kamilekbeznosa
k8s-health-checker check -n default
dns-cert-monitor check
azure-cost-reporter report --dry-run
```

Full documentation, configuration, and usage examples: **[python/README.md](python/README.md)**

---

## Bash Scripts

**Location:** [`bash/`](bash/)

Utility scripts for Linux environments — network diagnostics, health checks, Docker cleanup, SSL expiry checks, and port scanning.

| Script | Purpose |
|---|---|
| `health_check.sh` | Basic service/host health verification |
| `ssl_expiry_checker.sh` | Single-domain SSL certificate expiry check |
| `docker_janitor.sh` | Remove unused Docker resources |
| `net_diag.sh` | Network diagnostics |
| `ports_check.sh` | Port availability scanner |

> **Note:** `ssl_expiry_checker.sh` is the predecessor of `python/` → `dns-cert-monitor`, which adds multi-domain YAML config, retries, structured logging, and CI-friendly exit codes.

Details: [bash/README.MD](bash/README.MD)

---

## PowerShell Scripts

**Location:** [`Powershell/`](Powershell/)

Windows-focused automation — service monitoring, domain checks, Docker cleanup, and watchdog utilities.

| Script | Purpose |
|---|---|
| `service_checker.ps1` | Windows service status monitoring |
| `domain_checker.ps1` | Domain / DNS verification |
| `docker_janitor.ps1` | Docker resource cleanup on Windows |
| `watchdog.ps1` | Process/service watchdog |

Details: [Powershell/README.md](Powershell/README.md)

---

## CI/CD

Python changes trigger an automated pipeline:

- **Lint:** `ruff check` + `ruff format --check`
- **Test:** `pytest` with coverage gate (≥ 40%)
- **Trigger:** pushes and PRs affecting `python/**`

Workflow: [`.github/workflows/python-ci.yml`](.github/workflows/python-ci.yml)

---

## Author

**Kamil Kubajewski** — Junior DevOps Engineer  
[GitHub](https://github.com/kamilekbeznosa) · [LinkedIn](https://www.linkedin.com/in/kamil-kubajewski/)

---

## License

MIT
