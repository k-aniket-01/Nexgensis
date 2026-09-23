from collections.abc import Iterable
from app.utility import calculate_distance
from app.schemas import (
    AgentSchema, AgentStatsSchema, DeliveryInputSchema,
    DeliveryReportSchema, PackageSchema, Point, WarehouseSchema,
)


def normalize_input(raw_data: dict):

    raw_warehouses = raw_data.get("warehouses")
    raw_agents = raw_data.get("agents")
    raw_packages = raw_data.get("packages")

    if raw_warehouses is None:
        raise ValueError("Missing 'warehouses' section.")

    if raw_agents is None:
        raise ValueError("Missing 'agents' section.")

    if raw_packages is None:
        raise ValueError("Missing 'packages' section.")

    warehouses = normalize_locations(raw_warehouses, "warehouse")
    agents = normalize_locations(raw_agents, "agent")
    packages = normalize_packages(raw_packages)

    validate_unique_ids(warehouses, "warehouse")
    validate_unique_ids(agents, "agent")
    validate_unique_package_ids(packages)
    validate_package_warehouses(packages, warehouses)

    return DeliveryInputSchema(
        warehouses=warehouses,
        agents=agents,
        packages=packages,
    )


def normalize_locations(raw_data, entity_name: str):
    normalized = []

    if isinstance(raw_data, dict):
        for entity_id, location in raw_data.items():
            normalized.append(
                create_location_schema(
                    entity_id=entity_id,
                    location=location,
                    entity_name=entity_name,
                )
            )

    elif isinstance(raw_data, list):
        for index, item in enumerate(raw_data):
            if not isinstance(item, dict):
                raise ValueError(f"{entity_name}[{index}] must be an object.")
            normalized.append(
                create_location_schema(
                    entity_id=item.get("id"),
                    location=item.get("location"),
                    entity_name=entity_name,
                )
            )

    else:
        raise ValueError(f"'{entity_name}s' must be an object or list.")

    return normalized


def create_location_schema(entity_id, location,entity_name: str):

    if not isinstance(entity_id, str) or not entity_id.strip():
        raise ValueError(f"{entity_name} id must be a non-empty string.")

    if entity_name == "warehouse":
        return WarehouseSchema(
            id=entity_id,
            location=location,
        )

    return AgentSchema(
        id=entity_id,
        location=location,
    )


def normalize_packages(raw_packages: list):
    if not isinstance(raw_packages, list):
        raise ValueError("'packages' must be a list.")

    packages = []

    for index, package in enumerate(raw_packages):
        if not isinstance(package, dict):
            raise ValueError(f"packages[{index}] must be an object.")

        warehouse_id = package.get(
            "warehouse",
            package.get("warehouse_id"),
        )

        if warehouse_id is None:
            raise ValueError(f"packages[{index}] is missing warehouse information.")

        packages.append(
            PackageSchema(
                id=package.get("id"),
                warehouse=warehouse_id,
                destination=package.get(
                    "destination"
                ),
            )
        )

    return packages


def validate_unique_ids(entities: Iterable, entity_name: str):

    ids = [entity.id for entity in entities]

    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate {entity_name} ID found.")


def validate_unique_package_ids(packages: list[PackageSchema]):

    ids = [package.id for package in packages]

    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate package ID found.")


def validate_package_warehouses(packages: list[PackageSchema],
                                warehouses: list[WarehouseSchema]
                                ):
    warehouse_ids = {warehouse.id for warehouse in warehouses}

    for package in packages:
        if package.warehouse not in warehouse_ids:
            raise ValueError(
                f"Package '{package.id}' references "
                f"unknown warehouse "
                f"'{package.warehouse}'."
            )


def find_nearest_agent(agents: list[AgentSchema],warehouse: Point):
  
    if not agents:
        raise ValueError("At least one agent is required.")

    return min(
        agents,
        key=lambda agent: calculate_distance(
            agent.location,
            warehouse,
        ),
    )


def calculate_delivery_distance(
    agent: AgentSchema,
    warehouse: WarehouseSchema,
    package: PackageSchema,
):
    agent_to_warehouse = calculate_distance(agent.location, warehouse.location)
    warehouse_to_destination = calculate_distance(warehouse.location, package.destination)

    return (
        agent_to_warehouse
        + warehouse_to_destination
    )


def initialize_agent_stats(agents: list[AgentSchema]):

    return {
        agent.id: AgentStatsSchema(
            packages_delivered=0,
            total_distance=0,
            efficiency=None,
        )
        for agent in agents
    }


def simulate_delivery(data: DeliveryInputSchema):

    stats = initialize_agent_stats(data.agents)
    warehouses = {warehouse.id: warehouse for warehouse in data.warehouses}

    for package in data.packages:
        warehouse = warehouses[package.warehouse]

        nearest_agent = find_nearest_agent(
            data.agents,
            warehouse.location,
        )

        distance = calculate_delivery_distance(
            nearest_agent,
            warehouse,
            package,
        )

        agent_stats = stats[nearest_agent.id]
        agent_stats.packages_delivered += 1
        agent_stats.total_distance += distance

    calculate_efficiencies(stats)

    return stats


def calculate_efficiencies(stats: dict[str, AgentStatsSchema]):

    for agent_stats in stats.values():
        if agent_stats.packages_delivered == 0:
            agent_stats.efficiency = None
            continue

        agent_stats.efficiency = (
            agent_stats.total_distance
            / agent_stats.packages_delivered
        )

        agent_stats.total_distance = round(agent_stats.total_distance, 2)
        agent_stats.efficiency = round(agent_stats.efficiency, 2)


def build_report(stats: dict[str, AgentStatsSchema]):
    
    eligible_agents = {
        agent_id: agent_stats
        for agent_id, agent_stats in stats.items()
        if agent_stats.packages_delivered > 0
    }

    best_agent = None

    if eligible_agents:

        best_agent = min(
            eligible_agents,
            key=lambda agent_id: (
                eligible_agents[
                    agent_id
                ].efficiency,
                agent_id,
            ),
        )

    return DeliveryReportSchema(
        agents=stats,
        best_agent=best_agent,
    )