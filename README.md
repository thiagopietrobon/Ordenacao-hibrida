# Quicksort Híbrido: Análise de Desempenho em Python

Implementação e análise experimental de um algoritmo de ordenação híbrido que combina **Quicksort com pivô aleatório** e **Insertion Sort**.

O projeto investiga como diferentes valores de corte influenciam o tempo de execução, comparando o algoritmo híbrido com a versão pura do Quicksort.

## Objetivos

- Implementar o Quicksort puro com escolha aleatória do pivô.
- Implementar o Quicksort híbrido, utilizando Insertion Sort em sublistas pequenas.
- Avaliar diferentes valores de corte em vetores de 20.000 elementos.
- Comparar o desempenho das duas versões.
- Identificar o valor de corte com melhor resultado entre os testados.

## Relatório e resultados

A metodologia experimental, a tabela de tempos, o gráfico de desempenho, a comparação com o Quicksort puro e as conclusões estão documentados no **[RELATORIO.md](RELATORIO.md)**.

Os arquivos gerados pelo experimento também estão disponíveis no diretório `dados/`:

- [`resultados.csv`](dados/resultados.csv): dados numéricos das medições.
- [`resultados.png`](dados/resultados.png): gráfico de desempenho.

## Estrutura do projeto

```text
Ordenacao-hibrida/
├── algoritmos.py
├── benchmark.py
├── test_algoritmos.py
├── RELATORIO.md
└── dados/
    ├── resultados.csv
    └── resultados.png
```

| Arquivo | Descrição |
|---|---|
| `algoritmos.py` | Implementação do Insertion Sort, Quicksort puro e Quicksort híbrido. |
| `benchmark.py` | Executa os experimentos, compara os tempos e gera os resultados. |
| `test_algoritmos.py` | Testes de corretude dos algoritmos. |
| `RELATORIO.md` | Metodologia, resultados experimentais, gráfico e conclusões. |
| `dados/resultados.csv` | Dados numéricos do experimento principal. |
| `dados/resultados.png` | Gráfico de comparação do desempenho. |

## Requisitos

- Python 3.8 ou superior.
- Biblioteca `matplotlib`, utilizada para gerar o gráfico.

Instale a biblioteca com:

```bash
python -m pip install matplotlib
```

## Como executar

Execute os comandos a partir da pasta do projeto.

### 1. Executar os testes

```bash
python test_algoritmos.py
```

Os testes verificam diferentes situações, incluindo listas vazias, listas com um elemento, elementos repetidos, listas ordenadas, listas em ordem inversa e entradas aleatórias, além de diferentes valores de corte.

### 2. Executar o benchmark

```bash
python benchmark.py
```

Por padrão, o programa utiliza 20.000 elementos, 50 repetições e os valores de corte definidos no experimento.

Ao finalizar, apresenta os resultados no terminal e gera os arquivos CSV e PNG no diretório `dados/`.

### Opções do benchmark

| Opção | Valor padrão | Descrição |
|---|---|---|
| `--n` | `20000` | Quantidade de elementos do vetor. |
| `--reps` | `50` | Quantidade de repetições. |
| `--cortes` | `1 5 10 16 20 32 50 100 200` | Valores de corte avaliados. |
| `--semente` | `2024` | Semente utilizada para gerar os vetores aleatórios. |
| `--saida` | `resultados` | Nome-base dos arquivos gerados. |
| `--pasta` | `dados` | Diretório de saída dos resultados. |
| `--sem-grafico` | — | Executa sem gerar o gráfico. |

Exemplos:

```bash
# Benchmark mais curto
python benchmark.py --reps 10

# Benchmark com vetores maiores
python benchmark.py --n 100000 --reps 10

# Avaliar outros valores de corte
python benchmark.py --cortes 1 10 20 50 100
```

**Atenção:** uma nova execução pode substituir os arquivos de resultados existentes. Os tempos também podem variar conforme a máquina e as condições de execução.

## Utilização dos algoritmos

As funções podem ser importadas para outros programas Python:

```python
from algoritmos import rapida_pura, rapida_hibrida

dados = [5, 3, 8, 1, 9, 2]

print(rapida_pura(dados))
print(rapida_hibrida(dados, corte=20))
```

As duas funções retornam uma nova lista ordenada, sem modificar a lista original.

## Considerações finais

O projeto permite estudar a combinação de algoritmos de ordenação e avaliar experimentalmente como a escolha do valor de corte influencia o desempenho.

Para conhecer os resultados obtidos, consultar o gráfico e entender as conclusões do experimento, acesse o **[relatório completo](RELATORIO.md)**.