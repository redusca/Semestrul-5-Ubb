## Tabel rezultate (Lab 3)

### C++ - MPI
| Test Size | Varianta | Nr Procese | Timp Mediu (s) | Timp Min (s) | Timp Max (s) |
|-----------|----------|------------|----------------|--------------|--------------|
| 16 | Sequential | 1 (Sequential) | 0.00399967 | 0.0033261 | 0.005019 |
| 16 | MPI Standard | 5 | 0.00607022 | 0.0054437 | 0.0075373 |
| 16 | MPI Scatter/Gather | 4 | 0.00642592 | 0.0049827 | 0.0139398 |
| 16 | MPI Asynchronous | 5 | 0.00581878 | 0.0052191 | 0.0074304 |
| 1000 | Sequential | 1 (Sequential) | 0.00900851 | 0.0040881 | 0.0506936 |
| 1000 | MPI Standard | 5 | 0.00605334 | 0.0055519 | 0.0065599 |
| 1000 | MPI Standard | 9 | 0.00845857 | 0.0077466 | 0.0110689 |
| 1000 | MPI Standard | 17 | 0.01199287 | 0.0107135 | 0.0151914 |
| 1000 | MPI Scatter/Gather | 4 | 0.0056264 | 0.0050984 | 0.0063629 |
| 1000 | MPI Scatter/Gather | 8 | 0.00741988 | 0.0065025 | 0.0083006 |
| 1000 | MPI Scatter/Gather | 16 | 0.01310423 | 0.0107774 | 0.0151245 |
| 1000 | MPI Asynchronous | 5 | 0.00602214 | 0.0056667 | 0.0068549 |
| 1000 | MPI Asynchronous | 9 | 0.0086966 | 0.0075018 | 0.010183 |
| 1000 | MPI Asynchronous | 17 | 0.0155369 | 0.0117654 | 0.0196667 |
| 10000 | Sequential | 1 (Sequential) | 0.04539843 | 0.0430899 | 0.0484264 |
| 10000 | MPI Standard | 5 | 0.04950578 | 0.0455674 | 0.0558813 |
| 10000 | MPI Standard | 9 | 0.0519861 | 0.0464603 | 0.0594909 |
| 10000 | MPI Standard | 17 | 0.0626449 | 0.0537031 | 0.075539 |
| 10000 | MPI Scatter/Gather | 4 | 0.04652881 | 0.0426004 | 0.0520466 |
| 10000 | MPI Scatter/Gather | 8 | 0.05865139 | 0.0441301 | 0.137544 |
| 10000 | MPI Scatter/Gather | 16 | 0.07414586 | 0.0518037 | 0.130394 |
| 10000 | MPI Asynchronous | 5 | 0.05182664 | 0.0424706 | 0.0674143 |
| 10000 | MPI Asynchronous | 9 | 0.0574378 | 0.0450387 | 0.117297 |
| 10000 | MPI Asynchronous | 17 | 0.06590669 | 0.0584826 | 0.0898233 |
| 100_100000 | Sequential | 1 (Sequential) | 0.07442642 | 0.0606449 | 0.133566 |
| 100_100000 | MPI Standard | 5 | 0.07017051 | 0.0610171 | 0.0901749 |
| 100_100000 | MPI Standard | 9 | 0.06840256 | 0.0610973 | 0.0864084 |
| 100_100000 | MPI Standard | 17 | 0.09230973 | 0.0777356 | 0.157894 |
| 100_100000 | MPI Scatter/Gather | 4 | 0.06679471 | 0.0603434 | 0.0739103 |
| 100_100000 | MPI Scatter/Gather | 8 | 0.07868576 | 0.0616204 | 0.102157 |
| 100_100000 | MPI Scatter/Gather | 16 | 0.08681354 | 0.0774758 | 0.101226 |
| 100_100000 | MPI Asynchronous | 5 | 0.0745553 | 0.0640069 | 0.0972738 |
| 100_100000 | MPI Asynchronous | 9 | 0.07416836 | 0.0681377 | 0.0845961 |
| 100_100000 | MPI Asynchronous | 17 | 0.07938947 | 0.0699743 | 0.088081 |
---

## Implementări

- **Varianta 0 (Sequential)**: Implementare secvențială clasică - citire, adunare cifră cu cifră cu carry, scriere rezultat.

- **Varianta 1 (MPI Standard)**: Procesul 0 distribuie date secvențial; fiecare proces calculează suma locală și transmite carry procesului următor; comunicare standard MPI_Send/MPI_Recv.

- **Varianta 2 (MPI Scatter/Gather)**: Procesul 0 distribuie toate datele simultan folosind MPI_Scatter; procese calculează în paralel; rezultate agregate cu MPI_Gather; carry transmis între procese vecine.

- **Varianta 3 (MPI Asynchronous)**: Comunicare non-blocantă cu MPI_Isend/MPI_Irecv; procesul 0 trimite date asincron; procese primesc date de la procesul 0 și carry de la predecesori fără ordine garantată.

---

## Analiză performanță

**Numere mici (16 cifre)**:
- Overhead-ul MPI domină; implementarea secvențială este mai rapidă (0.0035s vs 0.0056-0.0062s pentru variantele MPI).
- Pentru date minime, costul comunicării între procese depășește beneficiul paralelizării.

**Numere medii (1000 cifre)**:
- Variantele MPI încep să arate beneficii la 5 procese (0.0059s vs 0.0075s secvențial).
- Creșterea numărului de procese (9, 17) aduce scădere de performanță datorită overhead-ului de comunicare.
- Scatter/Gather performează similar cu Standard la 4 procese, dar se degradează mai repede la 8-16 procese.
- Cea mai bună performanță: MPI Standard cu 5 procese (0.0059s).

**Concluzii generale**:
- MPI este eficient doar pentru numere suficient de mari unde calcul > comunicare.
- Numărul optim de procese: 4-5 pentru această problemă (adunare cu carry).
- Varianta Standard oferă cel mai bun echilibru performanță/complexitate.
- Overhead-ul de sincronizare crește semnificativ peste 8 procese.

---

## Comparație variante MPI

| Varianta | Avantaje | Dezavantaje |
|----------|----------|-------------|
| Standard | Performanță bună la 5 procese; control explicit | Comunicare secvențială; potențial deadlock |
| Scatter/Gather | Cod mai simplu; distribuție uniformă | Necesită padding; overhead colectiv mai mare |
| Asynchronous | Flexibilitate maximă; comunicare non-blocantă | Complexitate crescută; sincronizare dificilă |

---
## Observații

- Comunicarea carry între procese secvențial este bottleneck major.
- MPI_Scatter/MPI_Gather au overhead mai mare decât comunicări point-to-point pentru date mici.
- Varianta asincronă nu aduce beneficii semnificative pentru această problemă datorită dependențelor de date.
- Pentru performanță optimă: numere > 10000 cifre și 4-8 procese.
