def epsilon_clusters(values, eps):
    """
    tworzenie clusterow
    """
    indexed = sorted(enumerate(values, start=1), key=lambda x: x[1])

    clusters = []
    current = [indexed[0]]
    min_val = indexed[0][1]
    max_val = indexed[0][1]

    for idx, val in indexed[1:]:
        new_min = min(min_val, val)
        new_max = max(max_val, val)

        if new_max - new_min > eps:
            clusters.append(current)
            current = [(idx, val)]
            min_val = val
            max_val = val
        else:
            current.append((idx, val))
            min_val = new_min
            max_val = new_max

    clusters.append(current)
    return clusters


def plurality_vote(clusters):
    """
    najwieksze clustery
    """
    sizes = [len(c) for c in clusters]
    max_size = max(sizes)

    winners = [clusters[i] for i in range(len(clusters)) if sizes[i] == max_size]
    return winners


def formalized_plurality(values, eps):
    """
    zwraca wszyskie i wygrane clustery
    """
    clusters = epsilon_clusters(values, eps)
    winners = plurality_vote(clusters)
    return clusters, winners

def choose_one_value(plurality_clusters):
    """
    zwraca pierwsza liczbe najwiekszego clustera (w przypadku kliku, pierwszego)
    """
    cluster = plurality_clusters[0]
    return cluster[0][1]


if __name__ == "__main__":

    values = [0.486, 0.483, 0.530, 0.495, 0.489, 0.500, 0.481]
    eps = 0.01

    clusters, winners = formalized_plurality(values, eps)

    print("Wartosci:",values)

    print("\nEpsilon:",eps)

    print("\nClustery:")
    for c in clusters:
        print([f"x{idx}" for idx, val in c])

    print("\nWartosci clusterow:")
    for c in clusters:
        print([val for idx, val in c])

    print("\nWygrane clustery:")
    for w in winners:
        print([f"x{idx}" for idx, val in w])

    print("\nWartosci wygranych clusterow:")
    for w in winners:
        print([val for idx, val in w])

    print("\nWynik algorytmu:", choose_one_value(winners))
