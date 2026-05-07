def Calculation_of_C1(C2, V2, V1):
    if V1 == 0:
        print("Error: V1 cannot be zero, run again.")
        return None
    return (C2 * V2) / V1


def Calculation_of_V1(C1, C2, V2):
    if C1 == 0:
        print("Error: C1 cannot be zero, run again.")
        return None
    return (C2 * V2) / C1


def Calculation_of_C2(C1, V1, V2):
    if V2 == 0:
        print("Error: V2 cannot be zero, run again.")
        return None
    return (C1 * V1) / V2


def Calculation_of_V2(C1, V1, C2):
    if C2 == 0:
        print("Error: C2 cannot be zero, run again.")
        return None
    return (C1 * V1) / C2
