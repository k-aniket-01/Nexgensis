from app.schemas import AgentStatsSchema
from app.service import build_report


def test_best_agent():

    stats = {
        "A1": AgentStatsSchema(
            packages_delivered=2,
            total_distance=100,
            efficiency=50,
        ),
        "A2": AgentStatsSchema(
            packages_delivered=2,
            total_distance=80,
            efficiency=40,
        ),
        "A3": AgentStatsSchema(
            packages_delivered=1,
            total_distance=60,
            efficiency=60,
        ),
    }

    report = build_report(stats)

    assert report.best_agent == "A2"