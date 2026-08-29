"""Minimal typed query-plan model for Sprint 0.

This is intentionally small. It establishes the durable boundary between model output
and deterministic compilation without prematurely encoding the full DDKG query language.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EntityReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)
    text: str | None = None
    identifier: str | None = None


class QueryPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["0.1"] = "0.1"
    status: Literal["ready", "clarification_required", "unsupported"]
    intent: str = Field(min_length=1)
    entities: list[EntityReference] = Field(default_factory=list)
    result_limit: int = Field(default=50, ge=1, le=500)
    clarification_question: str | None = None
