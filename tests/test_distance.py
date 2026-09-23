from app.utility import calculate_distance


def test_distance_between_3_4_triangle():
    distance = calculate_distance(
        (0, 0),
        (3, 4),
    )

    assert distance == 5


def test_distance_between_same_point():
    distance = calculate_distance(
        (10, 10),
        (10, 10),
    )

    assert distance == 0