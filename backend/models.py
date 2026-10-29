"""
Data models and schemas for Refactor.ai.
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RefactorGoal(str, Enum):
    READABILITY = "readability"
    COMPLEXITY = "complexity"
    PERFORMANCE = "performance"
    POTENTIAL_BUGS = "potential_bugs"
    MAINTAINABILITY = "maintainability"
    ADD_COMMENTS = "add_comments"
    EXPLAIN_CODE = "explain_code"
    ADD_TYPES = "add_types"
    SECURITY = "security"
    MODERNIZE = "modernize"


class Language(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    CPP = "cpp"
    CSHARP = "csharp"
    SQL = "sql"
    AUTO = "auto"


class RefactorRequest(BaseModel):
    code: str = Field(..., min_length=5, max_length=50000, description="Source code to refactor")
    goal: RefactorGoal = Field(default=RefactorGoal.READABILITY, description="Primary goal of the refactoring")
    language: Language = Field(default=Language.AUTO, description="Source language (or auto)")
    context: Optional[str] = Field(default=None, max_length=2000, description="Optional extra instructions or context")


class RefactorResponse(BaseModel):
    original_code: str
    refactored_code: str
    language: str
    goal: str
    explanation: str
    explanations: List[str]
    improvements: List[str]
    risks: List[str]
    risks_and_tradeoffs: List[str]
    provider: str  # "gemini" | "nebius-nvidia" | "groq" | "demo"
    model: str
    tokens_used: int
    processing_ms: int
    demo_mode: bool = False
    warning: str = "Warning: AI-generated code requires human review and has not been executed or independently verified."


class HealthResponse(BaseModel):
    status: str
    version: str
    gemini_configured: bool
    gemini_model: str
    nebius_configured: bool
    nebius_model: str
    groq_configured: bool
    groq_model: str
    active_provider: str
    demo_mode: bool


class ConfigStatusResponse(BaseModel):
    version: str
    active_selection: str
    providers: dict
