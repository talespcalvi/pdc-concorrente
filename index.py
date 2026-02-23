from math import sqrt
import concurrent.futures
import multiprocessing
from timeit import default_timer as timer
import matplotlib.pyplot as plt


def eh_primo(x):
    """
    Retorna o proprio numero se for primo, None caso contrario.
    """
    if x < 2:
        return None
    if x == 2:
        return x
    if x % 2 == 0:
        return None

    limit = int(sqrt(x)) + 1
    for i in range(3, limit, 2):
        if x % i == 0:
            return None
    return x


def encontrar_primos_no_intervalo(inicio, quantidade, n_workers):
    """
    Versao otimizada usando map + chunksize
    """
    intervalo = range(inicio, inicio + quantidade)

    start_total = timer()

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
        # chunksize reduz overhead de comunicação
        resultados = executor.map(eh_primo, intervalo, chunksize=200)

        primos = [r for r in resultados if r is not None]

    tempo_total = timer() - start_total

    return primos, tempo_total


def main():
    _inicio = 10**13
    _quantidade = 1000  # Aumentado para gerar carga real
    _max_workers = multiprocessing.cpu_count()

    print(f"Testando intervalo: {_inicio:,} ate {_inicio + _quantidade:,}")
    print(f"Numero maximo de workers disponiveis: {_max_workers}\n")

    processadores = []
    tempos_totais = []

    for n_workers in range(1, _max_workers + 1):
        print(f"Testando com {n_workers} processo(s)")

        primos, t_total = encontrar_primos_no_intervalo(
            _inicio, _quantidade, n_workers
        )

        print(f"Primos encontrados: {len(primos)}")
        print(f"Tempo total: {t_total:8.4f} s")
        print("-" * 30)

        processadores.append(n_workers)
        tempos_totais.append(t_total)

    # ------------------ GRAFICO ------------------

    plt.figure(figsize=(8, 5))
    plt.plot(processadores, tempos_totais, marker='o')
    plt.xlabel('Numero de Processadores')
    plt.ylabel('Tempo Total (s)')
    plt.title('Desempenho vs Paralelismo (Lei de Amdahl)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
