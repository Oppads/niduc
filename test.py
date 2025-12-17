import numpy as np
import matplotlib.pyplot as plt


from modifiedSmoothingVoter import modified_smoothing_voter
from plurality import formalized_plurality as plurality_func
from plurality import choose_one_value as plurality_wynik
from FormalizedMajorityVoter import FormalizedMajorityVoter as MajorityVoter
from smoothingVoter import basic_smoothing_voter


class PluralityAdapter:
    def __init__(self, eps):
        self.eps = eps

    def vote(self, inputs):
        clusters, winners = plurality_func(inputs, self.eps)
        if not winners: return None
        return plurality_wynik(winners)


class BasicSmoothingAdapter:
    def __init__(self, eps, smoothing_b):
        self.eps = eps
        self.b = smoothing_b
        self.prev_output = 0.0  # Stan początkowy (sinus startuje od 0)

    def vote(self, inputs):
        result = basic_smoothing_voter(inputs, self.prev_output, self.eps, self.b)
        if result is not None:
            self.prev_output = result
        return result


class ModifiedSmoothingAdapter:
    def __init__(self, eps, base_b):
        self.eps = eps
        self.base_b = base_b
        self.prev_output = 0.0
        self.cumulative_threshold = base_b  # Stan początkowy progu

    def vote(self, inputs):
        result, new_thresh = modified_smoothing_voter(
            inputs, self.prev_output, self.eps, self.base_b, self.cumulative_threshold
        )
        self.cumulative_threshold = new_thresh  # Aktualizacja stanu progu
        if result is not None:
            self.prev_output = result
        return result




class VoterSimulation:
    def __init__(self, steps=200):
        self.steps = steps
        self.t = np.linspace(0, 4 * np.pi, steps)
        self.true_signal = np.sin(self.t)

        # Generowanie sygnałów
        self.s1 = self.true_signal + np.random.normal(0, 0.02, steps)
        self.s2 = self.true_signal + np.random.normal(0, 0.05, steps)
        self.s3 = self.true_signal + np.random.normal(0, 0.10, steps)

        self._inject_faults()

    def _inject_faults(self):
        # Awaria S3 zacina się
        self.s3[50:80] = 1.5

        # Awaria rozjazd S2 i S3
        self.s2[130:150] += 0.5
        self.s3[130:150] -= 0.5

    def run(self, eps=0.2, smoothing_b=0.3):
        print(f"Uruchamiam symulację (eps={eps}, b={smoothing_b})...")

        # Inicjalizacja Voterów
        maj_voter = MajorityVoter(eps)
        plu_voter = PluralityAdapter(eps)
        bas_voter = BasicSmoothingAdapter(eps, smoothing_b)
        mod_voter = ModifiedSmoothingAdapter(eps, smoothing_b)

        # Listy wyników
        res = {"maj": [], "plu": [], "bas": [], "mod": []}

        for i in range(self.steps):
            inputs = [self.s1[i], self.s2[i], self.s3[i]]

            res["maj"].append(maj_voter.vote(inputs))
            res["plu"].append(plu_voter.vote(inputs))
            res["bas"].append(bas_voter.vote(inputs))
            res["mod"].append(mod_voter.vote(inputs))

        self._plot_results(res, eps, smoothing_b)

    def _plot_results(self, res, eps, b):
        plt.figure(figsize=(12, 16))  # Wyższy wykres, bo więcej danych

        # 1. Wejścia
        plt.subplot(5, 1, 1)
        plt.title("Wejścia: 3 czujniki z błędami")
        plt.plot(self.t, self.s1, 'g-', alpha=0.5, label='S1')
        plt.plot(self.t, self.s2, 'b-', alpha=0.5, label='S2')
        plt.plot(self.t, self.s3, 'r-', alpha=0.5, label='S3')
        plt.plot(self.t, self.true_signal, 'k--', label='Idealny')
        plt.legend(loc='upper right')
        plt.grid(True)

        # 2. Majority
        plt.subplot(5, 1, 2)
        plt.title(f"Majority Voter (eps={eps})")
        plt.plot(self.t, res["maj"], 'o-', markersize=3, color='purple')
        plt.plot(self.t, self.true_signal, 'k--', alpha=0.2)
        plt.ylabel("Wyjście")
        plt.grid(True)

        # 3. Plurality
        plt.subplot(5, 1, 3)
        plt.title(f"Plurality Voter (eps={eps})")
        plt.plot(self.t, res["plu"], 'o-', markersize=3, color='orange')
        plt.plot(self.t, self.true_signal, 'k--', alpha=0.2)
        plt.ylabel("Wyjście")
        plt.grid(True)

        # 4. Basic Smoothing
        plt.subplot(5, 1, 4)
        plt.title(f"Basic Smoothing Voter (eps={eps}, b={b})")
        plt.plot(self.t, res["bas"], 'o-', markersize=3, color='teal')
        plt.plot(self.t, self.true_signal, 'k--', alpha=0.2)
        plt.ylabel("Wyjście")
        plt.grid(True)

        # 5. Modified Smoothing
        plt.subplot(5, 1, 5)
        plt.title(f"Modified Smoothing Voter (eps={eps}, base_b={b})")
        plt.plot(self.t, res["mod"], 'o-', markersize=3, color='magenta')
        plt.plot(self.t, self.true_signal, 'k--', alpha=0.2)
        plt.xlabel("Czas")
        plt.ylabel("Wyjście")
        plt.grid(True)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    sim = VoterSimulation(steps=200)
    # Przekazujemy też parametr b (smoothing threshold)
    sim.run(eps=0.2, smoothing_b=0.3)