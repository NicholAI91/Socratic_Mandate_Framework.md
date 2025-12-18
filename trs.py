"""
Trust Resilience Score™ (TRS) Engine
====================================

Copyright (c) 2025 Nicholas Reid Angell
Licensed under MIT License (code only)

Trust Resilience Score™ and TRS™ are trademarks of Nicholas Reid Angell.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import hashlib
import json


class TRSAxis(str, Enum):
    """Four axes of TRS measurement."""
    FRICTION_ENGAGEMENT = "friction_engagement"      # 40%
    VERIFICATION_ACTIONS = "verification_actions"    # 30%
    ACKNOWLEDGED_RESPONSIBILITY = "acknowledged_responsibility"  # 20%
    CORRECTION_CLARIFICATION = "correction_clarification"  # 10%


@dataclass
class TRSComponent:
    """Individual TRS component score."""
    axis: TRSAxis
    raw_score: float  # 0.0 - 1.0
    weight: float
    weighted_score: float
    details: dict = field(default_factory=dict)


@dataclass
class TRSSnapshot:
    """Immutable snapshot of TRS calculation."""
    session_id: str
    user_id: str
    timestamp: datetime
    
    # Component scores
    friction_engagement: float
    verification_actions: float
    acknowledged_responsibility: float
    correction_clarification: float
    
    # Composite
    composite_score: float
    
    # Anti-gaming flags
    gaming_detected: bool = False
    gaming_indicators: list = field(default_factory=list)
    
    # Hash chain for audit
    previous_hash: Optional[str] = None
    record_hash: Optional[str] = None
    
    def __post_init__(self):
        if self.record_hash is None:
            self.record_hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """Compute SHA-256 hash for immutable record."""
        data = {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "friction_engagement": self.friction_engagement,
            "verification_actions": self.verification_actions,
            "acknowledged_responsibility": self.acknowledged_responsibility,
            "correction_clarification": self.correction_clarification,
            "composite_score": self.composite_score,
            "gaming_detected": self.gaming_detected,
            "previous_hash": self.previous_hash,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


class TRSEngine:
    """
    Trust Resilience Score™ calculation engine.
    
    TRS Components:
    - Friction Engagement (40%): Quality of Socratic prompt responses
    - Verification Actions (30%): User-initiated fact-checking
    - Acknowledged Responsibility (20%): Explicit consent acknowledgments
    - Correction & Clarification (10%): User corrections of AI outputs
    """
    
    WEIGHTS = {
        TRSAxis.FRICTION_ENGAGEMENT: 0.40,
        TRSAxis.VERIFICATION_ACTIONS: 0.30,
        TRSAxis.ACKNOWLEDGED_RESPONSIBILITY: 0.20,
        TRSAxis.CORRECTION_CLARIFICATION: 0.10,
    }
    
    # Anti-gaming thresholds
    MIN_RESPONSE_TIME_MS = 2000  # Too fast = likely gaming
    MIN_QUALITY_RESPONSE_LENGTH = 20  # Characters
    
    def __init__(self, analyzer=None):
        self.analyzer = analyzer or DefaultTRSAnalyzer()
        self._previous_hash: Optional[str] = None
    
    async def calculate_trs(
        self,
        session_id: str,
        user_id: str,
        friction_response: Optional[str] = None,
        friction_prompt: Optional[str] = None,
        response_time_ms: Optional[int] = None,
        verification_count: int = 0,
        consent_acknowledged: bool = False,
        corrections_made: int = 0,
    ) -> TRSSnapshot:
        """
        Calculate TRS for a session interaction.
        
        Args:
            session_id: Unique session identifier
            user_id: User identifier
            friction_response: User's response to Socratic friction prompt
            friction_prompt: The friction prompt that was shown
            response_time_ms: Time taken to respond (for gaming detection)
            verification_count: Number of verification actions taken
            consent_acknowledged: Whether explicit consent was given
            corrections_made: Number of AI corrections submitted
        
        Returns:
            TRSSnapshot with all component scores and composite
        """
        gaming_indicators = []
        
        # 1. Friction Engagement (40%)
        friction_score = 0.0
        if friction_response:
            friction_score = self.analyzer.analyze_friction_response(
                friction_response, friction_prompt
            )
            
            # Gaming detection: too fast
            if response_time_ms and response_time_ms < self.MIN_RESPONSE_TIME_MS:
                gaming_indicators.append(f"response_too_fast:{response_time_ms}ms")
                friction_score *= 0.5  # Penalize
            
            # Gaming detection: too short
            if len(friction_response.strip()) < self.MIN_QUALITY_RESPONSE_LENGTH:
                gaming_indicators.append(f"response_too_short:{len(friction_response)}")
                friction_score *= 0.7  # Penalize
        
        # 2. Verification Actions (30%)
        verification_score = min(1.0, verification_count * 0.25)  # Cap at 4 actions
        
        # 3. Acknowledged Responsibility (20%)
        responsibility_score = 1.0 if consent_acknowledged else 0.0
        
        # 4. Correction & Clarification (10%)
        correction_score = min(1.0, corrections_made * 0.33)  # Cap at 3 corrections
        
        # Composite score
        composite = (
            friction_score * self.WEIGHTS[TRSAxis.FRICTION_ENGAGEMENT] +
            verification_score * self.WEIGHTS[TRSAxis.VERIFICATION_ACTIONS] +
            responsibility_score * self.WEIGHTS[TRSAxis.ACKNOWLEDGED_RESPONSIBILITY] +
            correction_score * self.WEIGHTS[TRSAxis.CORRECTION_CLARIFICATION]
        )
        
        # Create snapshot
        snapshot = TRSSnapshot(
            session_id=session_id,
            user_id=user_id,
            timestamp=datetime.utcnow(),
            friction_engagement=friction_score,
            verification_actions=verification_score,
            acknowledged_responsibility=responsibility_score,
            correction_clarification=correction_score,
            composite_score=composite,
            gaming_detected=len(gaming_indicators) > 0,
            gaming_indicators=gaming_indicators,
            previous_hash=self._previous_hash,
        )
        
        # Update hash chain
        self._previous_hash = snapshot.record_hash
        
        return snapshot


class DefaultTRSAnalyzer:
    """Default heuristic analyzer for TRS components."""
    
    # Keywords indicating quality engagement
    QUALITY_INDICATORS = [
        "understand", "acknowledge", "aware", "recognize",
        "confirm", "agree", "consent", "accept",
        "verify", "check", "confirm", "validate",
    ]
    
    # Keywords indicating verification behavior
    VERIFICATION_INDICATORS = [
        "source", "citation", "reference", "evidence",
        "proof", "documentation", "verify", "fact-check",
    ]
    
    # Keywords indicating correction behavior
    CORRECTION_INDICATORS = [
        "incorrect", "wrong", "error", "mistake",
        "actually", "correction", "clarify", "fix",
    ]
    
    def analyze_friction_response(
        self, 
        response: str, 
        prompt: Optional[str] = None
    ) -> float:
        """
        Analyze quality of friction response.
        
        Returns score 0.0 - 1.0 based on:
        - Length and substance
        - Presence of quality indicators
        - Semantic relevance to prompt
        """
        if not response:
            return 0.0
        
        response_lower = response.lower()
        score = 0.0
        
        # Base score from length (capped at 200 chars)
        length_score = min(1.0, len(response) / 200)
        score += length_score * 0.3
        
        # Quality indicator presence
        quality_count = sum(
            1 for indicator in self.QUALITY_INDICATORS
            if indicator in response_lower
        )
        quality_score = min(1.0, quality_count * 0.2)
        score += quality_score * 0.4
        
        # Sentence structure (has periods/complete thoughts)
        sentence_count = response.count('.') + response.count('!') + response.count('?')
        structure_score = min(1.0, sentence_count * 0.25)
        score += structure_score * 0.3
        
        return min(1.0, score)
    
    def detect_verification_intent(self, message: str) -> bool:
        """Check if message indicates verification behavior."""
        message_lower = message.lower()
        return any(
            indicator in message_lower 
            for indicator in self.VERIFICATION_INDICATORS
        )
    
    def detect_correction_intent(self, message: str) -> bool:
        """Check if message indicates correction behavior."""
        message_lower = message.lower()
        return any(
            indicator in message_lower
            for indicator in self.CORRECTION_INDICATORS
        )


__all__ = [
    "TRSEngine",
    "TRSSnapshot",
    "TRSComponent",
    "TRSAxis",
    "DefaultTRSAnalyzer",
]
