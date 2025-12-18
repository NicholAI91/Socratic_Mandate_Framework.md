# Socratic_Mandate_Framework.md

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![TRS Certified](https://img.shields.io/badge/TRS-Framework-purple.svg)](https://github.com/your-username/socratic-mandate)

**A Human-Centric AI Safety Framework for LLM Systems**

> *"The goal is not machine infallibility—it's human cognitive resilience."*

---

## Trademark Notice

**Socratic Mandate™**, **SocrAI:Verify™**, **Trust Resilience Score™**, **TRS™**, and **Socratic Green Team™** are trademarks of Nicholas Reid Angell.

**Angell's Laws** (the mathematical framework) is **open academic work** under MIT License with DOI — freely available for use with attribution.

This software is released under the MIT License, which applies to the **source code only**. The trademarks, certification programs, and associated methodologies are not covered by this license. See [TRADEMARKS.md](TRADEMARKS.md) for details.

For commercial licensing, certification, or enterprise support: [Contact](mailto:your-email@domain.com)

---

## What is the Socratic Mandate?

The Socratic Mandate is a comprehensive AI safety framework that shifts focus from the intractable goal of machine infallibility to the achievable goal of **human cognitive resilience**. 

Instead of trying to make AI "safe" (impossible to guarantee), we make humans **resistant to AI-induced cognitive harm** through structured protocols that enforce critical thinking, epistemic humility, and explicit accountability.

### The Five Pillars

| Pillar | Name | Function |
|--------|------|----------|
| **I** | Epistemic Humility | Force AI to signal uncertainty and knowledge limits |
| **II** | Cognitive Friction | Socratic checkpoints requiring active user engagement |
| **III** | Tiered Consent | Risk-based consent gateways with graduated requirements |
| **IV** | Zero-Trust Data | PII redaction, prompt injection detection, immutable audit logs |
| **V** | Organizational Accountability | Mandatory escalation to legal/security/ethics teams |

### Trust Resilience Score™ (TRS)

The framework includes a quantifiable metric for human-AI interaction health:

```
TRS Components:
├── Friction Engagement (40%) — Quality of Socratic prompt responses
├── Verification Actions (30%) — User-initiated fact-checking
├── Acknowledged Responsibility (20%) — Explicit consent acknowledgments
└── Correction & Clarification (10%) — User corrections of AI outputs
```

TRS functions as an **ESG-style score for AI systems**—enabling investors, insurers, and regulators to assess cognitive safety compliance.

---

## Quick Start

### Installation

```bash
pip install socratic-mandate
```

Or from source:

```bash
git clone https://github.com/your-username/socratic-mandate.git
cd socratic-mandate
pip install -e .
```

### Basic Usage

```python
from socratic_mandate import SocraticShell, TRSEngine

# Wrap any LLM with Socratic protections
shell = SocraticShell(
    provider="openai",  # or "anthropic", "ollama", "vllm"
    model="gpt-4"
)

# Process a query with full pillar enforcement
response = await shell.process(
    user_id="user_123",
    message="What medication should I take for my headache?",
    session_id="session_456"
)

# Response includes Socratic friction if topic is sensitive
print(response.requires_consent)  # True
print(response.consent_tier)      # "SENSITIVE"
print(response.friction_prompt)   # "Before I provide medical information..."
```

### TRS Calculation

```python
from socratic_mandate.trs import TRSEngine

engine = TRSEngine()

# Calculate TRS for a session
snapshot = await engine.calculate_trs(
    session_id="session_456",
    user_id="user_123",
    friction_response="I understand this is not medical advice...",
    friction_prompt="What is your understanding of AI limitations?",
    response_time_ms=8500
)

print(f"Composite TRS: {snapshot.composite_score}")
print(f"Friction Engagement: {snapshot.friction_engagement}")
```

---

## Architecture

```
socratic-mandate/
├── src/
│   ├── pillars/
│   │   ├── epistemic_humility.py    # Pillar I
│   │   ├── cognitive_friction.py    # Pillar II
│   │   ├── tiered_consent.py        # Pillar III
│   │   ├── zero_trust_data.py       # Pillar IV
│   │   └── accountability.py        # Pillar V
│   ├── trs/
│   │   ├── engine.py                # TRS calculation
│   │   ├── analyzer.py              # Behavioral analysis
│   │   └── reporter.py              # Forensic reports
│   ├── models/
│   │   ├── openai_provider.py
│   │   ├── anthropic_provider.py
│   │   └── local_provider.py        # Ollama, vLLM, llama.cpp
│   ├── storage/
│   │   └── worm.py                  # Immutable audit logs
│   └── auth/
│       └── middleware.py            # API key, rate limiting
├── docs/
├── tests/
└── examples/
```

---

## Features

### Pillar I: Epistemic Humility
- Automatic uncertainty signaling for low-confidence responses
- Domain-specific caveats (medical, legal, financial)
- Source attribution and knowledge boundary disclosure

### Pillar II: Cognitive Friction
- Context-aware Socratic prompts before high-stakes outputs
- Semantic quality control for user responses
- Adaptive friction based on engagement quality
- Temporal delays for consent acknowledgment

### Pillar III: Tiered Consent
- **DEFAULT**: Implicit consent for general queries
- **SENSITIVE**: Explicit acknowledgment for health/finance/legal
- **RESEARCH**: Written justification + supervisor approval
- **FORENSIC**: Full audit trail + mandatory escalation

### Pillar IV: Zero-Trust Data
- PII redaction (email, phone, SSN, credit cards, IP addresses)
- Prompt injection detection
- WORM (Write-Once-Read-Many) audit storage
- SHA-256 hash-chained records

### Pillar V: Organizational Accountability
- Automated escalation to Legal, Security, Ethics, Crisis teams
- Slack, PagerDuty, webhook integrations
- Session termination for security threats

---

## Deployment

### Docker

```bash
docker-compose up -d
```

### Kubernetes

```bash
kubectl apply -f k8s/
```

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...

# Optional
DATABASE_URL=postgresql://user:pass@host:5432/socratic
REDIS_URL=redis://localhost:6379
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
PAGERDUTY_API_KEY=...
```

---

## API Reference

### REST API

```
POST /v1/chat          # Process message with Socratic shell
POST /v1/consent       # Submit consent acknowledgment
GET  /v1/audit/{id}    # Retrieve audit record
POST /v1/trs/calculate # Calculate TRS for session
GET  /v1/trs/report/{session_id}  # Get forensic TRS report
```

### Full API documentation: [docs/api.md](docs/api.md)

---

## TRS™ Certification

Organizations implementing the Socratic Mandate can apply for official TRS™ Certification:

| Level | Requirements |
|-------|-------------|
| **Bronze** | Implements Pillars I-III |
| **Silver** | Implements all five pillars |
| **Gold** | Third-party audit verification |
| **Platinum** | Continuous monitoring + forensic audit |

Certification enables:
- EU AI Act compliance documentation
- Favorable AI liability insurance terms
- "TRS Certified" badge for marketing
- Investor-grade safety metrics

[Apply for Certification →](mailto:your-email@domain.com)

---

## Research & Publications

The Socratic Mandate framework is based on research by Nicholas Reid Angell (Research Name: Zoey A.):

- *The Socratic Mandate: A Human-Centric AI Safety Framework* (2025)
- *Trust Resilience Score: Quantifying Human-AI Interaction Health* (2025)
- *Angell's Laws: Mathematical Foundations of Cognitive Safety* (2025)

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Note: By contributing, you agree that your contributions will be licensed under MIT. Trademark usage in contributions must comply with [TRADEMARKS.md](TRADEMARKS.md).

---

## License

MIT License — see [LICENSE](LICENSE)

**Trademark Notice**: The names Socratic Mandate™, SocrAI™, Trust Resilience Score™, TRS™, and Angell's Laws™ are trademarks of Nicholas Reid Angell and are NOT covered by the MIT License. See [TRADEMARKS.md](TRADEMARKS.md).

---

## Author

**Nicholas Reid Angell**  
Creator of the Socratic Mandate™ Framework

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Nicholas Reid Angell](https://linkedin.com/in/your-profile)
- Research: Zoey A.

---

<p align="center">
  <i>The machine serves not just as a tool, but as a proactive, ethical governor of human critical judgment.</i>
</p>
