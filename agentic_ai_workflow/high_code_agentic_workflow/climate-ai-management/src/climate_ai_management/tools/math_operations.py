def find_total(
    coe1: float,
    coe2: float,
    coe3: float
) -> float:
    """Calculate the sum of Scope 1, Scope 2 and Scope 3 emissions."""

    return coe1 + coe2 + coe3


def find_difference_coe2(
    calculated_total: float,
    declared_total: float
) -> float:
    """Calculate the difference between calculated and declared emissions."""

    return calculated_total - declared_total