# Quicksort híbrido (rápida + inserção) em Python

Implementa a ordenação rápida com pivô aleatório (partição em menores / iguais / maiores),
a versão híbrida que chama a inserção em pedaços pequenos (parâmetro `corte`) e mede
qual corte dá o melhor tempo. Os resultados e a análise estão em [`RELATORIO.md`](RELATORIO.md).

## Requisitos

- Python 3.8 ou superior.
- `matplotlib` — **opcional**, só para gerar o gráfico (`pip install matplotlib`).
  Sem ele o programa roda normalmente, imprime a tabela e salva o CSV; apenas avisa que o gráfico não foi gerado.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `algoritmos.py` | `insercao`, `rapida_pura` e `rapida_hibrida(lista, corte)` |
| `test_algoritmos.py` | testes de corretude (vazio, 1 elemento, repetidos, ordenado, inverso, aleatórios) |
| `benchmark.py` | medição de tempo, comparação com a pura, verificação do corte = 1, CSV e gráfico |
| `RELATORIO.md` | tabela, gráfico e conclusões |
| `dados/` | pasta com os dados gerados (criada automaticamente pelo `benchmark.py`) |
| `dados/resultados.csv` / `.png` | saída da rodada principal (20 000 elementos) |
| `dados/resultados_semente7.csv` | rodada de conferência com outra semente |
| `dados/extras_cortes_grandes.csv` / `.png` | cortes bem maiores (500 a 5000), para ilustrar o custo quadrático |

## Como executar

Na pasta do projeto:

```bash
# 1) testes de corretude (rápido, deve imprimir "Todos os testes passaram.")
python test_algoritmos.py

# 2) experimento completo: 20 000 elementos, cortes 1, 5, 10, 16, 20, 32, 50, 100, 200
python benchmark.py
```

O passo 2 leva algumas dezenas de segundos (varia com a máquina). Ele imprime a tabela de tempos, o melhor corte, o ganho sobre a
rápida pura e a verificação do corte = 1, e grava `dados/resultados.csv` e `dados/resultados.png` (a pasta `dados/` é criada se não existir).

### Opções do `benchmark.py`

| Opção | Padrão | Descrição |
|---|---|---|
| `--n` | `20000` | tamanho do vetor |
| `--reps` | `50` | quantidade de vetores aleatórios distintos (mais repetições = menos ruído) |
| `--cortes` | `1 5 10 16 20 32 50 100 200` | cortes a testar |
| `--semente` | `2024` | semente dos vetores (mesma semente = mesmos vetores) |
| `--saida` | `resultados` | nome-base dos arquivos de saída (`.csv` e `.png`) |
| `--pasta` | `dados` | pasta onde os arquivos de saída são gravados |
| `--sem-grafico` | — | não gera o gráfico |

Exemplos:

```bash
python benchmark.py --reps 10                       # rodada rápida, mais ruidosa
python benchmark.py --n 100000 --reps 10            # vetor maior
python benchmark.py --cortes 1 100 500 1000 --saida teste   # grava dados/teste.csv e dados/teste.png
```

## Usando as funções no seu código

```python
from algoritmos import rapida_pura, rapida_hibrida

dados = [5, 3, 8, 1, 9, 2]
print(rapida_pura(dados))              # [1, 2, 3, 5, 8, 9]
print(rapida_hibrida(dados, corte=16)) # [1, 2, 3, 5, 8, 9]
```

As funções devolvem uma **nova** lista; a original não é alterada.

## Observações sobre os tempos

Os tempos absolutos dependem da máquina, da versão do Python e da carga do sistema (o desvio entre
repetições é de vários milissegundos). Por isso o benchmark usa a **mediana** de várias repetições,
os mesmos vetores para todas as variantes e ordem embaralhada. Ao reproduzir, espere números
diferentes dos do relatório, mas a **forma da curva** (queda, faixa plana e depois subida) deve se manter.