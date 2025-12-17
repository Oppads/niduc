from typing import List, Optional


def distance(a: float, b: float) -> float:
    #dystans między a,b: d(a,b) = |a-b|
    return abs(a - b)


def basic_smoothing_voter(
    variants: List[float],
    prev_output: float,
    voter_threshold: float,
    smoothing_threshold: float
) -> Optional[float]:
    """
    Implementacja Basic Smoothing Voter
    parametry:
    variants: lista wyników wariantów [d1, d2, ..., dN]
    prev_output: poprzedni poprawny wynik votera (X)
    voter_threshold: próg większości (λ)
    smoothing_threshold: próg wygładzania (b)
    return: wynik votera lub brak wyniku (None)
    """

    # sortowanie
    AS = sorted(variants)
    N = len(AS)
    m = (N + 1) // 2

    # sprawdzenie czy istnieje większość
    for j in range(N - m + 1):
        if distance(AS[j], AS[j + m - 1]) <= voter_threshold:
            # jeśli większość jest znaleziona → wybieramy środkowy element przedziału
            return AS[j]

    # brak większości → wybór najbliższego do poprzedniego wyniku
    closest = min(variants, key=lambda x: distance(x, prev_output))

    # test wygładzania
    if distance(closest, prev_output) <= smoothing_threshold:
        return closest

    # case braku wyniku
    return None