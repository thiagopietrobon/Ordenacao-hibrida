# Relatório — Quicksort híbrido (rápida + inserção)

## 1. O que foi feito

- `rapida_pura`: quicksort com **pivô aleatório** e partição em **menores / iguais / maiores**.
- `rapida_hibrida(lista, corte)`: igual à anterior, mas pedaços com **menos que `corte` elementos** são ordenados por **inserção**. O `corte` é parâmetro da função.
- `benchmark.py`: mede o tempo com **20 000 inteiros aleatórios**, variando o corte em 1, 5, 10, 16, 20, 32, 50, 100 e 200, e compara com a rápida pura.

**Metodologia.** 50 vetores aleatórios distintos (valores em [0, 10⁶]); todas as variantes ordenam exatamente os mesmos vetores, em ordem embaralhada a cada repetição (para nenhuma variante ser favorecida por rodar sempre primeiro ou último). Cada resultado é conferido contra `sorted()`. O tempo reportado é a **mediana** das 50 repetições (mais robusta a picos de ruído do sistema que a média); a média e o desvio-padrão também aparecem na tabela. Ambiente: Python 3.12, execução em uma única CPU — os tempos absolutos mudam de máquina para máquina, as proporções são o que importa.

## 2. Resultados

| Corte | Mediana (ms) | Média ± desvio (ms) | Ganho sobre a rápida pura (negativo = mais lenta) |
|------:|-------------:|--------------------:|-------------------------:|
| **pura** | 35,69 | 37,21 ± 4,63 | — |
| 1 | 36,37 | 39,20 ± 8,43 | -1,9% |
| 5 | 31,76 | 33,39 ± 4,67 | +11,0% |
| 10 | 27,01 | 28,59 ± 4,40 | +24,3% |
| 16 | 25,65 | 27,81 ± 4,79 | +28,1% |
| **20** | **25,24** | 26,46 ± 3,53 | +29,3% |
| 32 | 25,95 | 28,14 ± 5,49 | +27,3% |
| 50 | 27,10 | 28,97 ± 5,88 | +24,1% |
| 100 | 32,57 | 34,44 ± 5,52 | +8,7% |
| 200 | 46,81 | 50,29 ± 9,65 | -31,2% |

![Tempo em função do corte](dados/resultados.png)

Dados completos em `dados/resultados.csv`.

## 3. Qual corte deu o melhor tempo?

Na rodada principal, o melhor foi **corte = 20**, com **25,24 ms**, contra **35,69 ms** da rápida pura: um **ganho de 29,3%** (a híbrida leva ~71% do tempo da pura, ou seja, é cerca de 1,41× mais rápida).

**Atenção ao ler esse “melhor”:** os cortes 16, 20 e 32 ficam praticamente empatados (25,65, 25,24 e 25,95 ms) — a diferença entre eles é bem menor que o desvio-padrão (~4–5 ms). Para conferir, repeti o experimento com outra semente (`--semente 7`, em `dados/resultados_semente7.csv`): o vencedor foi o corte **32** (28,1% de ganho), mas de novo com 16, 20 e 32 separados por cerca de 1% entre si. A conclusão confiável não é “o corte ideal é 20”, e sim:

> **A faixa ideal fica entre 16 e 32, com ganho de cerca de 27% a 29% sobre a rápida pura.**

**Por que o ganho acontece.** Com n = 20 000, o quicksort puro sorteia e particiona cerca de 13 mil pedaços (13 230 na verificação da seção 5), muitos deles com poucos elementos. Para um pedaço de 3 ou 4 elementos, o custo fixo de cada chamada em Python — sortear pivô, montar três listas, concatenar — é bem maior que o trabalho útil. A inserção resolve esses pedaços sem recursão nem listas auxiliares, e como o pedaço é pequeno, seu custo quadrático ainda é desprezível.

**Por que o ganho para de crescer perto de 16–32.** A cada aumento do corte, economiza-se menos recursão (já eliminamos as chamadas mais numerosas) e a inserção fica mais cara. Por volta de 16–32 as duas forças se equilibram; daí em diante a curva sobe.

## 4. O que acontece com cortes grandes demais?

A inserção custa O(k²) por pedaço de tamanho k. Com corte grande, os pedaços entregues à inserção também são grandes, e o custo total passa a ser aproximadamente **proporcional a n · corte** — enquanto a economia de chamadas recursivas já se esgotou. Na curva principal:

- corte = 100: o ganho encolhe para 8,7%;
- o ponto de empate com a rápida pura fica em torno de **120** (interpolação entre 100 e 200);
- corte = 200: a híbrida fica **31% mais lenta** que a pura.

Para ver até onde isso vai, rodei também cortes bem maiores (15 repetições, `dados/extras_cortes_grandes.csv` / `.png`):

| Corte | Mediana (ms) | Tempo relativo à rápida pura |
|------:|-------------:|-----------------------------:|
| **pura** | 34,33 | 1,0× |
| 100 | 32,24 | 0,9× |
| 200 | 45,84 | 1,3× |
| 500 | 99,46 | 2,9× |
| 1000 | 212,20 | 6,2× |
| 2000 | 458,98 | 13,4× |
| 5000 | 1285,43 | 37,4× |

O tempo cresce aproximadamente de forma linear com o corte (cerca de 0,2–0,26 ms por unidade de corte, nesta máquina), exatamente como previsto por n · corte. No limite, com corte maior que o vetor inteiro, a “híbrida” vira uma inserção pura sobre 20 000 elementos, com custo quadrático.

## 5. Corte = 1 se comporta como a rápida pura?

**Sim.** Evidências:

1. **Por construção:** a inserção só é chamada para pedaços com 2 ≤ tamanho < corte. Com corte = 1 essa condição nunca é verdadeira, então o código percorre exatamente os mesmos caminhos da rápida pura. (Pedaços de 0 ou 1 elemento já estão ordenados e são devolvidos direto, nas duas versões; por isso o corte = 2 também equivale à pura.)
2. **Verificação experimental** (`verifica_corte_1` em `benchmark.py`, mesma semente de pivôs nas duas versões, n = 20 000):
   - resultado idêntico entre pura, híbrida com corte = 1 e `sorted()`: **sim**;
   - pivôs sorteados: **13 230** na pura e **13 230** na híbrida com corte = 1;
   - chamadas à inserção com corte = 1: **0**.
3. **Tempo:** 36,37 ms (corte = 1) contra 35,69 ms (pura). A híbrida com corte = 1 saiu 1,5% a 1,9% mais lenta nas três rodadas que fiz (principal, `--semente 7` e a dos cortes grandes). Essa diferença é muito menor que o desvio-padrão (4–8 ms) e é compatível com o pequeno custo extra de receber os parâmetros `corte` e `stats` e testar `n < corte` a cada chamada — o algoritmo, porém, é o mesmo.

## 6. Conclusões

- Combinar métodos funciona: um corte entre 16 e 32 deixou a ordenação cerca de **27–29% mais rápida** que a rápida pura.
- A curva tem forma de “U”: pouco corte desperdiça recursão em pedaços minúsculos; muito corte entrega à inserção pedaços onde o custo quadrático domina.
- O valor ótimo depende da linguagem e da implementação. Aqui, em Python (onde cada chamada recursiva e cada lista auxiliar têm custo alto), a faixa ótima foi 16–32; em outra linguagem ou com partição in-place ela pode ser bem diferente, então **meça** em vez de copiar este número.