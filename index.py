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
    Encontra numeros primos em um intervalo usando ProcessPoolExecutor
    Retorna: (lista de primos, tempo de coleta de resultados, tempo total)
    """
    intervalo = range(inicio, inicio + quantidade)

    start_total = timer()
    primos = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(eh_primo, num) for num in intervalo]

        start_coleta = timer()

        for future in concurrent.futures.as_completed(futures):
            resultado = future.result()
            if resultado is not None:
                primos.append(resultado)

        tempo_coleta = timer() - start_coleta

    tempo_total = timer() - start_total

    return primos, tempo_coleta, tempo_total


def main():
    _inicio = 10**13
    _quantidade = 100000
    _max_workers = multiprocessing.cpu_count()

    print(f"Testando intervalo: {_inicio:,} ate {_inicio + _quantidade:,}")
    print(f"Numero maximo de workers disponiveis: {_max_workers}\n")

    processadores = []
    tempos_totais = []

    for n_workers in range(1, _max_workers + 1):
        print(f"\nTestando com {n_workers} processo(s)")

        primos, t_coleta, t_total = encontrar_primos_no_intervalo(
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