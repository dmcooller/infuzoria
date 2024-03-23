def try_float(x: str) -> float:
    try:
        return float(x)
    except:
        return 0
