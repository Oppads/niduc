from typing import List, Optional


def distance(a: float, b: float) -> float:
    #dystans między a,b: d(a,b) = |a-b|
    return abs(a - b)

def modified_smoothing_voter(
    variants: List[float],
    prev_output: float,
    voter_threshold: float,
    base_smoothing_threshold: float,
    cumulative_threshold: float
) -> (Optional[float], float):
    """
    Implementacja Modified Smoothing Voter

    basic smoothing rozszerzony o parametry:
    base_smoothing_threshold: bazowy próg wygładzania (b)
    cumulative_threshold: aktualny kumulacyjny próg wygładzania
    return: (wynik lub None, nowy próg kumulacyjny)
    """

    AS = sorted(variants)
    N = len(AS)
    m = (N + 1) // 2

    # Sprawdzenie większości
    for j in range(N - m + 1):
        if distance(AS[j], AS[j + m - 1]) <= voter_threshold:
            # sukces → reset progu
            return AS[j], base_smoothing_threshold

    # Brak większości → wybór najbliższego wyniku
    closest = min(variants, key=lambda x: distance(x, prev_output))

    if distance(closest, prev_output) <= cumulative_threshold:
        # znalezienie wyniku → reset progu
        return closest, base_smoothing_threshold

    # Brak wyniku → aktualizacja progu kumulacyjnego
    if closest > prev_output:
        cumulative_threshold += base_smoothing_threshold
    else:
        cumulative_threshold -= base_smoothing_threshold

    return None, cumulative_threshold