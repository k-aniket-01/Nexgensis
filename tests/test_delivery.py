from app.schemas import (
    AgentSchema,
    PackageSchema,
    WarehouseSchema,
)
from app.service import (
    calculate_delivery_distance,
    find_nearest_agent,
)


def test_find_nearest_agent():

    agents = [
        AgentSchema(
            id="A1",
            location=(5, 5),
        ),
        AgentSchema(
            id="A2",
            location=(60, 60),
        ),
        AgentSchema(
            id="A3",
            location=(95, 30),
        ),
    ]

    warehouse = (0, 0)

    nearest = find_nearest_agent(
        agents,
        warehouse,
    )

    assert nearest.id == "A1"


def test_delivery_distance():

    agent = AgentSchema(
        id="A1",
        location=(5, 5),
    )

    warehouse = WarehouseSchema(
        id="W1",
        location=(0, 0),
    )

    package = PackageSchema(
        id="P1",
        warehouse="W1",
        destination=(30, 40),
    )

    distance = calculate_delivery_distance(
        agent,
        warehouse,
        package,
    )

    assert round(distance, 2) == 57.07