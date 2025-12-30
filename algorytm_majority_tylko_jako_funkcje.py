import math


def create_clusters(values, epsilon):
    """
    Tworzy klastry, w których wartości nie różnią się
    o więcej niż epsilon (max - min klastra).
    """
    if not values:
        return []

    sorted_vals = sorted(values)
    clusters = []
    current_cluster = [sorted_vals[0]]

    for val in sorted_vals[1:]:
        if (val - current_cluster[0]) <= epsilon:
            current_cluster.append(val)
        else:
            clusters.append(current_cluster)
            current_cluster = [val]

    clusters.append(current_cluster)
    return clusters


def vote(inputs, epsilon):
    """
    Zwraca średnią z klastra większościowego albo None
    """
    n = len(inputs)
    if n == 0:
        return None

    clusters = create_clusters(inputs, epsilon)

    # największy klaster
    clusters.sort(key=len, reverse=True)
    largest_cluster = clusters[0]

    threshold = math.ceil((n + 1) / 2)

    if len(largest_cluster) >= threshold:
        return sum(largest_cluster) / len(largest_cluster)
    else:
        return None
