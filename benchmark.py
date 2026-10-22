"""Mede o tempo da rápida híbrida variando o corte e compara com a rápida pura.

Uso:
    python benchmark.py                       # padrão: 20 000 elementos, 30 repetições
    python benchmark.py --n 50000 --reps 10
    python benchmark.py --cortes 1 8 16 64 --saida extra
    python benchmark.py --pasta outra_pasta

CSV e gráfico são gravados na pasta `dados/` (criada se não existir).
"""
import argparse
import csv
import gc
import os
import random
import statistics
import time

from algoritmos import rapida_pura, rapida_hibrida

CORTES_PADRAO = [1, 5, 10, 16, 20, 32, 50, 100, 200]


def cronometra(funcao):
    gc.collect()
    t0 = time.perf_counter()
    resultado = funcao()
    return time.perf_counter() - t0, resultado


class RngContador(random.Random):
    """Gerador que conta quantos pivôs foram sorteados (um por pedaço particionado)."""
    sorteios = 0

    def randrange(self, *a, **k):
        self.sorteios += 1
        return super().randrange(*a, **k)


def verifica_corte_1(n, semente):
    """Confirma que corte = 1 se comporta como a rápida pura (mesma semente de pivôs)."""
    gerador = random.Random(semente)
    dados = [gerador.randint(0, 10**6) for _ in range(n)]
    rng_pura, rng_hib = RngContador(42), RngContador(42)
    stats = {}
    pura = rapida_pura(dados, rng_pura)
    hib = rapida_hibrida(dados, 1, rng_hib, stats)
    return {
        "mesmo_resultado_que_sorted": pura == hib == sorted(dados),
        "pivos_sorteados_pura": rng_pura.sorteios,
        "pivos_sorteados_hibrida_corte_1": rng_hib.sorteios,
        "chamadas_a_insercao_com_corte_1": stats.get("insercoes", 0),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20_000, help="tamanho do vetor")
    ap.add_argument("--reps", type=int, default=50, help="vetores aleatórios distintos")
    ap.add_argument("--cortes", type=int, nargs="+", default=CORTES_PADRAO)
    ap.add_argument("--semente", type=int, default=2024)
    ap.add_argument("--saida", default="resultados", help="nome-base dos arquivos de saída")
    ap.add_argument("--pasta", default="dados", help="pasta onde CSV e gráfico são gravados")
    ap.add_argument("--sem-grafico", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.pasta, exist_ok=True)
    base = os.path.join(args.pasta, args.saida)
    configs = ["pura"] + list(args.cortes)
    tempos = {c: [] for c in configs}
    gerador = random.Random(args.semente)

    print(f"n = {args.n}, repetições = {args.reps}, cortes = {args.cortes}")
    for rep in range(args.reps):
        dados = [gerador.randint(0, 10**6) for _ in range(args.n)]
        esperado = sorted(dados)
        ordem = configs[:]
        gerador.shuffle(ordem)  # evita favorecer quem roda primeiro/último
        for c in ordem:
            rng = random.Random(rep)  # mesma semente de pivôs para todos
            if c == "pura":
                t, r = cronometra(lambda: rapida_pura(dados, rng))
            else:
                t, r = cronometra(lambda: rapida_hibrida(dados, c, rng))
            assert r == esperado, f"resultado incorreto para {c}"
            tempos[c].append(t)
        print(f"  repetição {rep + 1}/{args.reps} ok", end="\r")
    print()

    med_pura = statistics.median(tempos["pura"])
    linhas = []
    for c in configs:
        v = tempos[c]
        med = statistics.median(v)
        linhas.append({
            "corte": c,
            "mediana_s": med,
            "media_s": statistics.mean(v),
            "desvio_s": statistics.stdev(v) if len(v) > 1 else 0.0,
            "minimo_s": min(v),
            "ganho_vs_pura_%": (med_pura - med) / med_pura * 100,
        })

    with open(f"{base}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)

    print(f"\nTabela salva em {base}.csv")
    print(f"\n{'corte':>6} {'mediana (ms)':>13} {'média (ms)':>11} {'desvio (ms)':>12} {'ganho':>8}")
    for l in linhas:
        print(f"{str(l['corte']):>6} {l['mediana_s']*1e3:13.2f} {l['media_s']*1e3:11.2f} "
              f"{l['desvio_s']*1e3:12.2f} {l['ganho_vs_pura_%']:7.1f}%")

    melhor = min(linhas[1:], key=lambda l: l["mediana_s"])
    print(f"\nMelhor corte: {melhor['corte']} "
          f"({melhor['mediana_s']*1e3:.2f} ms; ganho de {melhor['ganho_vs_pura_%']:.1f}% sobre a pura)")

    if 1 in args.cortes:
        print("\nVerificação corte = 1 vs rápida pura (mesma semente de pivôs):")
        for k, v in verifica_corte_1(args.n, args.semente).items():
            print(f"  {k}: {v}")

    if not args.sem_grafico:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib não instalado: gráfico não gerado (pip install matplotlib).")
            return
        xs = [l["corte"] for l in linhas[1:]]
        ys = [l["mediana_s"] * 1e3 for l in linhas[1:]]
        er = [l["desvio_s"] * 1e3 for l in linhas[1:]]
        fig, ax = plt.subplots(figsize=(8, 4.8))
        ax.errorbar(xs, ys, yerr=er, marker="o", capsize=3, label="Rápida híbrida (mediana ± desvio)")
        ax.axhline(med_pura * 1e3, color="tab:red", linestyle="--", label="Rápida pura (mediana)")
        ax.plot(melhor["corte"], melhor["mediana_s"] * 1e3, "g*", markersize=16, label=f"Melhor: corte = {melhor['corte']}")
        ax.set_xscale("log")
        ax.set_xticks(xs)
        ax.set_xticklabels([str(x) for x in xs])
        ax.set_xlabel("corte (escala logarítmica)")
        ax.set_ylabel("tempo (ms)")
        ax.set_title(f"Tempo de ordenação em função do corte (n = {args.n:,}".replace(",", ".") + ")")
        ax.grid(alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(f"{base}.png", dpi=150)
        print(f"Gráfico salvo em {base}.png")


if __name__ == "__main__":
    main()
    