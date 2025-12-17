import math


class FormalizedMajorityVoter:

    def __init__(self, epsilon):
        self.epsilon = epsilon

    def _create_clusters(self, values):

        #Metoda tworząca klastry, w której wartości nie są różne o wiecej niz epsilon

        if not values:
            return []

        sorted_vals = sorted(values)
        clusters = []
        current_cluster = [sorted_vals[0]]

        for val in sorted_vals[1:]:
            # Sprawdzamy rozpiętość klastra (max - min)
            if (val - current_cluster[0]) <= self.epsilon:
                current_cluster.append(val)
            else:
                clusters.append(current_cluster)
                current_cluster = [val]

        clusters.append(current_cluster)
        return clusters

    def vote(self, inputs):

        #Metoda głosująca, zwracająca None, lub klastra większościowego

        n = len(inputs)
        if n == 0:
            return None

        # Tworzenie klastrów
        clusters = self._create_clusters(inputs)

        # Znalezienie największego klastra
        clusters.sort(key=len, reverse=True)
        largest_cluster = clusters[0]

        # Warunek większości
        threshold = math.ceil((n + 1) / 2)

        if len(largest_cluster) >= threshold:
            # Sukces
            return sum(largest_cluster) / len(largest_cluster)
        else:
            # Porażka
            return None



if __name__ == "__main__":
    # Ustawiamy epsilon
    eps = 0.2
    voter = FormalizedMajorityVoter(epsilon=eps)

    print(f"TEST Formalized Majority Voter (epsilon={eps})\n")

    in1 = [1.0, 1.1, 0.95]
    print(f"Wejście: {in1}")
    print(f"Wynik: {voter.vote(in1)}\n")

    in2 = [0.5, 5.0, 0.55]
    print(f"Wejście: {in2}")
    print(f"Wynik: {voter.vote(in2)}\n")

    in3 = [1.0, 1.5, 2.1]
    print(f"Wejście: {in3}")
    print(f"Wynik: {voter.vote(in3)}")