from typing import TypeAlias

from pydantic import BaseModel, ConfigDict, Field, field_validator


Point: TypeAlias = tuple[float, float]


class PackageSchema(BaseModel):
    """
    Represents a package that needs to be delivered.
    """

    model_config = ConfigDict(extra="ignore")

    id: str = Field(min_length=1)
    warehouse: str = Field(min_length=1)
    destination: Point

    @field_validator("destination")
    @classmethod
    def validate_destination(cls, value: Point) -> Point:
        x, y = value

        if not (-1000 <= x <= 1000):
            raise ValueError(
                "destination x-coordinate must be between -1000 and 1000"
            )

        if not (-1000 <= y <= 1000):
            raise ValueError(
                "destination y-coordinate must be between -1000 and 1000"
            )

        return value


class AgentSchema(BaseModel):
    """
    Represents a delivery agent.
    """

    id: str = Field(min_length=1)
    location: Point


class WarehouseSchema(BaseModel):
    """
    Represents a warehouse.
    """

    id: str = Field(min_length=1)
    location: Point


class DeliveryInputSchema(BaseModel):
    """
    Complete normalized input structure.
    """

    warehouses: list[WarehouseSchema]
    agents: list[AgentSchema]
    packages: list[PackageSchema]


class AgentStatsSchema(BaseModel):
    """
    Statistics generated for one agent.
    """

    packages_delivered: int = Field(ge=0)
    total_distance: float = Field(ge=0)
    efficiency: float | None = Field(
        default=None,
        ge=0,
    )


class DeliveryReportSchema(BaseModel):
    """
    Final assignment report.
    """

    agents: dict[str, AgentStatsSchema]
    best_agent: str | None