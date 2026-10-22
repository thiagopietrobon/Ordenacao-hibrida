import random


def insercao(lista):
    """Ordenação por inserção. Ordena a lista recebida (cópia) e a devolve."""
    v = list(lista)
    for i in range(1, len(v)):
        chave = v[i]
        j = i - 1
        while j >= 0 and v[j] > chave:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = chave
    return v


def rapida_pura(lista, rng=random):
    """Quicksort com pivô aleatório e partição em menores / iguais / maiores."""
    if len(lista) <= 1:
        return list(lista)
    pivo = lista[rng.randrange(len(lista))]
    menores = [x for x in lista if x < pivo]
    iguais = [x for x in lista if x == pivo]
    maiores = [x for x in lista if x > pivo]
    return rapida_pura(menores, rng) + iguais + rapida_pura(maiores, rng)


def rapida_hibrida(lista, corte=16, rng=random, stats=None):
    """Quicksort que delega à inserção os pedaços com menos de `corte` elementos.

    corte : tamanho abaixo do qual o pedaço é ordenado por inserção.
            Com corte <= 2 a inserção nunca é chamada (pedaços de 0 ou 1
            elemento já estão ordenados), logo o comportamento é o da rápida pura.
    stats : dicionário opcional para contar chamadas (usado só na verificação).
    """
    if stats is not None:
        stats["chamadas"] = stats.get("chamadas", 0) + 1
    n = len(lista)
    if n <= 1:
        return list(lista)
    if n < corte:
        if stats is not None:
            stats["insercoes"] = stats.get("insercoes", 0) + 1
        return insercao(lista)
    pivo = lista[rng.randrange(n)]
    menores = [x for x in lista if x < pivo]
    iguais = [x for x in lista if x == pivo]
    maiores = [x for x in lista if x > pivo]
    return (rapida_hibrida(menores, corte, rng, stats)
            + iguais
            + rapida_hibrida(maiores, corte, rng, stats))
