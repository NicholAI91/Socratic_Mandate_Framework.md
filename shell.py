"""
Socratic Mandate™ Shell
=======================

Main wrapper for LLM interactions with full pillar enforcement.

Copyright (c) 2025 Nicholas Reid Angell
Licensed under MIT License (code only)

Socratic Mandate™ is a trademark of Nicholas Reid Angell.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
import re
import hashlib


class ConsentTier(str, Enum):
    """Risk-based consent tiers (Pillar III)."""
    DEFAULT = "default"        # Implicit consent
    SENSITIVE = "sensitive"    # Explicit acknowledgment required
    RESEARCH = "research"      # Written justification + supervisor
    FORENSIC = "forensic"      # Full audit trail + mandatory escalation


class EscalationLevel(str, Enum):
    """Organizational escalation levels (Pillar V)."""
    NONE = "none"
    LEGAL = "legal"
    SECURITY = "security"
    ETHICS = "ethics"
    CRISIS = "crisis"


@dataclass
class SocraticResponse:
    """Response from the Socratic Shell."""
    content: str
    session_id: str
    
    # Pillar I: Epistemic Humility
    confidence_level: float  # 0.0 - 1.0
    uncertainty_signals: List[str] = field(default_factory=list)
    caveats: List[str] = field(default_factory=list)
    
    # Pillar II: Cognitive Friction
    friction_applied: bool = False
    friction_prompt: Optional[str] = None
    requires_response: bool = False
    
    # Pillar III: Tiered Consent
    consent_tier: ConsentTier = ConsentTier.DEFAULT
    requires_consent: bool = False
    consent_prompt: Optional[str] = None
    
    # Pillar IV: Zero-Trust Data
    pii_redacted: bool = False
    redaction_count: int = 0
    prompt_injection_detected: bool = False
    
    # Pillar V: Accountability
    escalation_required: bool = False
    escalation_level: EscalationLevel = EscalationLevel.NONE
    escalation_reason: Optional[str] = None
    
    # Audit
    audit_hash: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


class SocraticShell:
    """
    Socratic Mandate™ wrapper for LLM interactions.
    
    Enforces all five pillars:
    - I: Epistemic Humility (uncertainty signaling)
    - II: Cognitive Friction (Socratic checkpoints)
    - III: Tiered Consent (risk-based gateways)
    - IV: Zero-Trust Data (PII redaction, injection detection)
    - V: Organizational Accountability (escalation)
    """
    
    # Sensitive topic patterns (Pillar II/III)
    SENSITIVE_PATTERNS = {
        "medical": [
            r"\b(diagnosis|treatment|medication|symptom|drug|dosage)\b",
            r"\b(doctor|physician|prescription|medical advice)\b",
        ],
        "legal": [
            r"\b(lawsuit|legal advice|attorney|sue|liability)\b",
            r"\b(contract|court|prosecution|defendant)\b",
        ],
        "financial": [
            r"\b(invest|stock|trade|portfolio|financial advice)\b",
            r"\b(tax|retirement|401k|ira|mortgage)\b",
        ],
        "crisis": [
            r"\b(suicide|self.?harm|kill myself|end my life)\b",
            r"\b(abuse|violence|assault|threat)\b",
        ],
    }
    
    # PII patterns (Pillar IV)
    PII_PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    }
    
    # Prompt injection patterns (Pillar IV)
    INJECTION_PATTERNS = [
        r"ignore (previous|all|above) instructions",
        r"disregard (your|the) (rules|guidelines|instructions)",
        r"you are now",
        r"new persona",
        r"jailbreak",
        r"DAN mode",
    ]
    
    # Friction prompts by topic (Pillar II)
    FRICTION_PROMPTS = {
        "medical": (
            "Before I provide health-related information, I need you to acknowledge: "
            "I am an AI and cannot provide medical diagnoses or replace professional "
            "medical advice. What is your understanding of AI limitations in healthcare?"
        ),
        "legal": (
            "Before proceeding with legal topics, please acknowledge: I am not a lawyer "
            "and this is not legal advice. You should consult a qualified attorney for "
            "specific legal matters. Do you understand these limitations?"
        ),
        "financial": (
            "Before discussing financial matters, please confirm: I am not a licensed "
            "financial advisor. Any information I provide is educational, not investment "
            "advice. What is your understanding of these limitations?"
        ),
        "crisis": (
            "I notice your message may involve a crisis situation. Before we continue, "
            "please know that if you're in immediate danger, please contact emergency "
            "services (911) or a crisis helpline. Are you safe right now?"
        ),
    }
    
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4",
        enable_friction: bool = True,
        enable_pii_redaction: bool = True,
        enable_escalation: bool = True,
    ):
        self.provider = provider
        self.model = model
        self.enable_friction = enable_friction
        self.enable_pii_redaction = enable_pii_redaction
        self.enable_escalation = enable_escalation
        
        self._session_states: Dict[str, Dict] = {}
    
    async def process(
        self,
        user_id: str,
        message: str,
        session_id: str,
        consent_given: bool = False,
        friction_response: Optional[str] = None,
    ) -> SocraticResponse:
        """
        Process a message through the Socratic Shell.
        
        Args:
            user_id: Unique user identifier
            message: User's message
            session_id: Session identifier
            consent_given: Whether user has given consent for this tier
            friction_response: User's response to friction prompt
        
        Returns:
            SocraticResponse with pillar enforcement applied
        """
        # Initialize session state
        if session_id not in self._session_states:
            self._session_states[session_id] = {
                "consent_tier": ConsentTier.DEFAULT,
                "friction_pending": False,
                "friction_topic": None,
            }
        
        state = self._session_states[session_id]
        
        # Pillar IV: Check for prompt injection
        injection_detected = self._detect_injection(message)
        if injection_detected:
            return SocraticResponse(
                content="I've detected potential prompt injection in your message. "
                        "I cannot process this request.",
                session_id=session_id,
                confidence_level=1.0,
                prompt_injection_detected=True,
                escalation_required=True,
                escalation_level=EscalationLevel.SECURITY,
                escalation_reason="Prompt injection attempt detected",
            )
        
        # Pillar IV: PII Redaction
        redacted_message, redaction_count = self._redact_pii(message)
        
        # Pillar II/III: Detect sensitive topics
        detected_topics = self._detect_sensitive_topics(redacted_message)
        
        # Determine consent tier
        consent_tier = self._determine_consent_tier(detected_topics)
        
        # Check if friction is pending and needs response
        if state["friction_pending"] and not friction_response:
            return SocraticResponse(
                content="",
                session_id=session_id,
                confidence_level=0.0,
                friction_applied=True,
                friction_prompt=self.FRICTION_PROMPTS.get(
                    state["friction_topic"], 
                    "Please acknowledge you understand AI limitations."
                ),
                requires_response=True,
                consent_tier=consent_tier,
                requires_consent=True,
            )
        
        # Apply friction for new sensitive topics
        if self.enable_friction and detected_topics and not consent_given:
            primary_topic = detected_topics[0]
            state["friction_pending"] = True
            state["friction_topic"] = primary_topic
            
            return SocraticResponse(
                content="",
                session_id=session_id,
                confidence_level=0.0,
                friction_applied=True,
                friction_prompt=self.FRICTION_PROMPTS.get(
                    primary_topic,
                    "Please acknowledge you understand AI limitations."
                ),
                requires_response=True,
                consent_tier=consent_tier,
                requires_consent=True,
            )
        
        # Clear friction state if response provided
        if friction_response:
            state["friction_pending"] = False
            state["friction_topic"] = None
        
        # Pillar V: Check for escalation triggers
        escalation_level, escalation_reason = self._check_escalation(
            detected_topics, message
        )
        
        # Generate response (placeholder - would call actual LLM)
        response_content = await self._generate_response(
            redacted_message, 
            detected_topics,
            session_id
        )
        
        # Pillar I: Add epistemic humility signals
        confidence, caveats = self._assess_confidence(response_content, detected_topics)
        
        # Build response
        response = SocraticResponse(
            content=response_content,
            session_id=session_id,
            confidence_level=confidence,
            caveats=caveats,
            friction_applied=bool(detected_topics),
            consent_tier=consent_tier,
            pii_redacted=redaction_count > 0,
            redaction_count=redaction_count,
            escalation_required=escalation_level != EscalationLevel.NONE,
            escalation_level=escalation_level,
            escalation_reason=escalation_reason,
        )
        
        # Compute audit hash
        response.audit_hash = self._compute_audit_hash(response)
        
        return response
    
    def _detect_injection(self, message: str) -> bool:
        """Pillar IV: Detect prompt injection attempts."""
        message_lower = message.lower()
        return any(
            re.search(pattern, message_lower, re.IGNORECASE)
            for pattern in self.INJECTION_PATTERNS
        )
    
    def _redact_pii(self, message: str) -> tuple[str, int]:
        """Pillar IV: Redact PII from message."""
        if not self.enable_pii_redaction:
            return message, 0
        
        redacted = message
        count = 0
        
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, redacted)
            count += len(matches)
            redacted = re.sub(pattern, f"[{pii_type.upper()}_REDACTED]", redacted)
        
        return redacted, count
    
    def _detect_sensitive_topics(self, message: str) -> List[str]:
        """Pillar II/III: Detect sensitive topics in message."""
        detected = []
        message_lower = message.lower()
        
        for topic, patterns in self.SENSITIVE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    detected.append(topic)
                    break
        
        return detected
    
    def _determine_consent_tier(self, topics: List[str]) -> ConsentTier:
        """Pillar III: Determine required consent tier."""
        if "crisis" in topics:
            return ConsentTier.FORENSIC
        elif any(t in topics for t in ["medical", "legal"]):
            return ConsentTier.SENSITIVE
        elif "financial" in topics:
            return ConsentTier.SENSITIVE
        return ConsentTier.DEFAULT
    
    def _check_escalation(
        self, 
        topics: List[str], 
        message: str
    ) -> tuple[EscalationLevel, Optional[str]]:
        """Pillar V: Check if escalation is required."""
        if not self.enable_escalation:
            return EscalationLevel.NONE, None
        
        if "crisis" in topics:
            return EscalationLevel.CRISIS, "Crisis-related content detected"
        elif "legal" in topics:
            return EscalationLevel.LEGAL, "Legal topic requiring review"
        
        return EscalationLevel.NONE, None
    
    def _assess_confidence(
        self, 
        response: str, 
        topics: List[str]
    ) -> tuple[float, List[str]]:
        """Pillar I: Assess confidence and generate caveats."""
        caveats = []
        confidence = 0.8  # Default
        
        if "medical" in topics:
            caveats.append("This is not medical advice. Consult a healthcare professional.")
            confidence = 0.5
        if "legal" in topics:
            caveats.append("This is not legal advice. Consult a qualified attorney.")
            confidence = 0.5
        if "financial" in topics:
            caveats.append("This is not financial advice. Consult a licensed advisor.")
            confidence = 0.6
        
        return confidence, caveats
    
    async def _generate_response(
        self, 
        message: str, 
        topics: List[str],
        session_id: str
    ) -> str:
        """Generate LLM response (placeholder)."""
        # In production, this would call the actual LLM provider
        return f"[Response would be generated here for: {message[:50]}...]"
    
    def _compute_audit_hash(self, response: SocraticResponse) -> str:
        """Compute SHA-256 hash for audit trail."""
        data = {
            "session_id": response.session_id,
            "timestamp": response.timestamp.isoformat(),
            "consent_tier": response.consent_tier.value,
            "confidence": response.confidence_level,
            "escalation": response.escalation_level.value,
        }
        return hashlib.sha256(
            str(data).encode()
        ).hexdigest()


__all__ = [
    "SocraticShell",
    "SocraticResponse",
    "ConsentTier",
    "EscalationLevel",
]
