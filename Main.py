from plurality import formalized_plurality as plurality
from plurality import choose_one_value as pluralityWynik
from FormalizedMajorityVoter import FormalizedMajorityVoter as majority


values = [0.486, 0.483, 0.530, 0.495, 0.489, 0.500, 0.481]
eps = 0.01

clusters, winners = plurality(values, eps)
print(f"Plurality wynik: {pluralityWynik(winners)}")

voter = majority(eps)
print(f"Majority voter: {voter.vote(values)}")