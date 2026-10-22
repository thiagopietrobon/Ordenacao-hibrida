"""Testes de corretude. Execute: python test_algoritmos.py"""
import random
from algoritmos import insercao, rapida_pura, rapida_hibrida

CORTES = [1, 2, 5, 10, 16, 20, 32, 50, 100, 200]


def casos():
    rng = random.Random(1)
    yield []
    yield [7]
    yield [2, 2, 2, 2]
    yield list(range(50))
    yield list(range(50, 0, -1))
    for n in (2, 3, 10, 37, 500):
        yield [rng.randint(0, 20) for _ in range(n)]       # muitos repetidos
        yield [rng.randint(0, 10**6) for _ in range(n)]    # poucos repetidos


def main():
    for caso in casos():
        esperado = sorted(caso)
        original = list(caso)
        assert insercao(caso) == esperado
        assert rapida_pura(caso, random.Random(0)) == esperado
        for c in CORTES:
            assert rapida_hibrida(caso, c, random.Random(0)) == esperado, (c, caso)
        assert caso == original, "a lista original não pode ser alterada"
    print("Todos os testes passaram.")


if __name__ == "__main__":
    main()
