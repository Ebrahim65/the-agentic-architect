# The Agentic Architect — Code

Official code repository for **The Agentic Architect: A Practical Guide to Building Production AI Systems** by **Ebrahim Pooe**.

This repository contains the Python examples, exercises, and project implementations referenced throughout the guide.

The guide is designed to move from Python foundations and LLM fundamentals through workflow engineering, tool use, RAG, agent architecture, AI skills, multi-agent systems, MCP, safety, evaluation, and production deployment.

> **Status:** First edition / living project  
> **Author:** Ebrahim Pooe

---

## What this repository is

The code in this repository is intended to be used alongside _The Agentic Architect_. The examples are deliberately practical and progressively build toward production-oriented AI systems.

The guide's progression is:

| Module | Topic                                      |
| ------ | ------------------------------------------ |
| 0      | Engineering Environment                    |
| 1      | Python for AI Engineering                  |
| 2      | LLM Fundamentals                           |
| 3      | Workflow Engineering and Automation Design |
| 4      | Tool Use and Function Calling              |
| 5      | RAG and Memory Systems                     |
| 6      | Agent Design Patterns                      |
| 7      | Designing AI Skills                        |
| 8      | Multi-Agent Systems                        |
| 9      | Model Context Protocol (MCP)               |
| 10     | AI Safety, Security, and Guardrails        |
| 11     | Evaluation and Observability               |
| 12     | AI Systems in Production                   |
| —      | Capstone and Optional Projects             |

The guide uses three recurring business scenarios:

- **Clarity** — customer/product assistance
- **HireStream** — recruitment workflow automation
- **LexGuard** — enterprise regulatory and compliance intelligence

These scenarios provide progressively more demanding environments in which the architectural concepts are applied.

---

## Repository structure

The repository is organized around the progression of the guide rather than around a single application.

```text
the-agentic-architect/
│
├── module-00-engineering-environment/
├── module-01-python-for-ai-engineering/
├── module-02-llm-fundamentals/
├── module-03-workflow-engineering/
├── module-04-tool-use/
├── module-05-rag-and-memory/
├── module-06-agent-design/
├── module-07-ai-skills/
├── module-08-multi-agent-systems/
├── module-09-mcp/
├── module-10-safety-security-guardrails/
├── module-11-evaluation-observability/
├── module-12-production/
│
├── projects/
│   ├── project-01/
│   ├── project-02/
│   ├── project-03/
│   └── project-04/
│
├── capstone/
│
├── optional-projects/
│
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

Some directories may not be included as of the release of this guide. Only essential code snippets have been provided in this repository.
The exact directory names may evolve as the repository is maintained.

---

## Requirements

The examples use Python and the guide's recommended development workflow uses [`uv`](https://docs.astral.sh/uv/).

You will generally need:

- Python 3.12+
- `uv`
- An API key for the model provider used by the example
- Git

Some examples introduce additional dependencies such as:

- OpenAI-compatible clients
- Pydantic
- HTTP clients
- MCP
- FastAPI
- vector/database tooling
- evaluation and observability tooling

Each project should document any additional requirements it introduces.

---

## Getting started

Clone the repository:

```bash
git clone <repository-url>
cd the-agentic-architect
```

If the repository uses a root `pyproject.toml`:

```bash
uv sync
```

Create your local environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Add the required API credentials to `.env`.

**Never commit `.env` or API keys to Git.**

Then run an example from the relevant module or project:

```bash
uv run <example>.py
```

Refer to the corresponding section of _The Agentic Architect_ for the purpose of the example, expected behaviour, and exercises.

---

## Model access

The guide uses OpenRouter and OpenAI-compatible APIs in many of its examples so that the underlying architectural patterns can be demonstrated without tying the material to a single model provider.

The specific model used by an example may change over time. Treat model names as implementation details rather than architectural requirements.

Where an example specifies a model, check the accompanying code and guide section for the current configuration.

---

## Projects

The guide contains four compulsory projects that progressively consolidate the material.

### Project 1 — Clarity Product Assistant

Build a tool-using product assistant for the Clarity scenario.

The project introduces the transition from simple LLM calls to agents that can interact with external capabilities.

### Project 2 — HireStream Screening Agent

Build a CV screening agent using ReAct and Reflection.

The system accepts a CV and job description, uses multiple tools, produces a structured recommendation, and applies guardrails and evaluation.

### Project 3 — Multi-Agent Document Processor

Build a multi-agent regulatory document processor for LexGuard using MCP.

The system includes an MCP server, a supervisor, specialist agents, source citations, and communication logging.

### Project 4 — Production Deployment

Deploy one of the preceding systems as a production-oriented API.

The project introduces:

- FastAPI
- API authentication
- rate limiting
- cost tracking
- retry logic
- structured logging
- request IDs
- deployment
- tracing
- trust and explainability documentation

---

## Learning philosophy

The repository follows the same principles as the guide:

**Understand before abstracting.**

Start with the underlying mechanism before introducing frameworks.

**Build before trusting.**

An agent that works in a demonstration is not necessarily an agent that works reliably.

**Design for failure.**

Tool errors, malformed inputs, model failures, prompt injection, runaway execution, cost overruns, and unexpected outputs are part of the engineering problem.

**Keep humans in the loop where appropriate.**

Autonomy is not automatically the goal. The appropriate level of automation depends on the risk and reversibility of the action.

**Treat evaluation and observability as engineering infrastructure.**

If you cannot measure what your system is doing, you cannot reliably improve it.

---

## Security

Never commit:

- API keys
- passwords
- database credentials
- private tokens
- production connection strings
- personal data

Use environment variables and `.env` files for local secrets.

If you discover a security issue in the repository, please report it responsibly rather than publishing credentials or exploit details in an issue.

---

## Disclaimer

The examples in this repository are educational implementations accompanying _The Agentic Architect_. They are not automatically production-ready merely because they demonstrate a production-oriented architectural pattern.

Before deploying an implementation to real users or handling sensitive information, conduct appropriate security, privacy, reliability, cost, and compliance reviews.

AI model behaviour, APIs, libraries, and recommended tooling change quickly. Some examples may require updates as their underlying dependencies evolve.

---

## Contributing

This repository is primarily the companion codebase for the guide.

Suggestions, corrections, improvements, and discussions are welcome.

If you find an issue with an example:

1. Check the corresponding section of the guide.
2. Confirm that your environment and dependencies match the documented requirements.
3. Open an issue describing the problem, including the relevant module/project and error message.
4. Do not include API keys or other secrets in the issue.

---

## About the author

**Ebrahim Pooe** is a software engineer and AI systems builder interested in the intersection of artificial intelligence, software engineering, systems architecture, and practical business applications.

_The Agentic Architect_ is an independent publication exploring the engineering discipline required to move beyond AI demonstrations and build reliable intelligent systems.

---

## The guide

**The Agentic Architect**  
_A Practical Guide to Building Production AI Systems_

Written by **Ebrahim Pooe**

The companion code in this repository is intended to evolve alongside future editions of the guide.
