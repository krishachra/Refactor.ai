"""
Configuration management for Refactor.ai.
Supports:
1. Google Gemini API (Primary Development Provider - eligible for Free Tier)
2. Nebius Token Factory (NVIDIA Nemotron - Mandatory Hackathon Provider)
3. Groq (Secondary / Fast Prototyping)
4. Offline Deterministic Demo Mode
"""
import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    # Provider selection: "auto", "gemini", "nebius", "groq", "demo"
    AI_PROVIDER: str = Field(default="auto")
    
    # Primary Development Provider: Google Gemini API
    GEMINI_API_KEY: str = Field(default="")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash")
    GEMINI_BASE_URL: str = Field(default="https://generativelanguage.googleapis.com/v1beta/models/")
    
    # Mandatory Hackathon Compliance Provider: Nebius Token Factory (NVIDIA Nemotron)
    NEBIUS_API_KEY: str = Field(default="")
    NEBIUS_BASE_URL: str = Field(default="https://api.tokenfactory.nebius.com/v1/")
    NEBIUS_MODEL: str = Field(default="nebius/nvidia/Nemotron-3_5-Lightning")
    
    # Secondary / Fast Prototyping: Groq
    GROQ_API_KEY: str = Field(default="")
    GROQ_BASE_URL: str = Field(default="https://api.groq.com/openai/v1/")
    GROQ_MODEL: str = Field(default="llama-3.1-8b-instant")
    
    # Application settings
    APP_VERSION: str = Field(default="1.1.0")
    MAX_CODE_LENGTH: int = Field(default=50000)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    ALLOWED_ORIGINS: str = Field(default="http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173")

    @classmethod
    def load_from_env(cls) -> "Settings":
        # Search for .env file in project root or backend dir
        potential_env_paths = [
            os.path.join(os.path.dirname(__file__), ".env"),
            os.path.join(os.path.dirname(__file__), "..", ".env"),
            os.path.abspath(".env")
        ]
        
        for env_path in potential_env_paths:
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip("'\"")
                            if k not in os.environ:
                                os.environ[k] = v

        return cls(
            AI_PROVIDER=os.getenv("AI_PROVIDER", "auto"),
            GEMINI_API_KEY=os.getenv("GEMINI_API_KEY", ""),
            GEMINI_MODEL=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            GEMINI_BASE_URL=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/models/"),
            NEBIUS_API_KEY=os.getenv("NEBIUS_API_KEY", ""),
            NEBIUS_BASE_URL=os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"),
            NEBIUS_MODEL=os.getenv("NEBIUS_MODEL", "nebius/nvidia/Nemotron-3_5-Lightning"),
            GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
            GROQ_BASE_URL=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1/"),
            GROQ_MODEL=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            APP_VERSION=os.getenv("APP_VERSION", "1.1.0"),
            MAX_CODE_LENGTH=int(os.getenv("MAX_CODE_LENGTH", "50000")),
            HOST=os.getenv("HOST", "0.0.0.0"),
            PORT=int(os.getenv("PORT", "8000")),
            ALLOWED_ORIGINS=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173")
        )
