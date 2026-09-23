from typing import TypeAlias

from pydantic import BaseModel, ConfigDict, Field, field_validator


Point: TypeAlias = tuple[float, float]


class PackageSchema(BaseModel):
    id: str = Field(min_length=1)
    warehouse: str = Field(min_length=1)
    destination: Point

    model_config = ConfigDict(extra="ignore")
    
    @field_validator("destination")
    @classmethod
    def validate_destination(cls, value: Point) -> Point:
        x, y = value

        if not (-1000 <= x <= 1000):
            raise ValueError("destination x-coordinate must be between -1000 and 1000")

        if not (-1000 <= y <= 1000):
            raise ValueError("destination y-coordinate must be between -1000 and 1000")

        return value


class AgentSchema(BaseModel):
    id: str = Field(min_length=1)
    location: Point


class WarehouseSchema(BaseModel):
    id: str = Field(min_length=1)
    location: Point


class DeliveryInputSchema(BaseModel):
    warehouses: list[WarehouseSchema]
    agents: list[AgentSchema]
    packages: list[PackageSchema]


class AgentStatsSchema(BaseModel):
    packages_delivered: int = Field(ge=0)
    total_distance: float = Field(ge=0)
    efficiency: float | None = Field(default=None, ge=0)


class DeliveryReportSchema(BaseModel):
    agents: dict[str, AgentStatsSchema]
    best_agent: str | None