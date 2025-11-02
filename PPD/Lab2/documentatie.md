## Tabel rezultate (Lab 2)

### Java

| Tip Matrice | Nr threads | Timp executie (ns) | Timp executie (s) |
|-------------|------------|--------------------|-------------------|
| Matrice 10x10 | secvential | 91650 ns | 0.000092 |
| Matrice 10x10 | 2 | 4769730 ns | 0.004770 |
| Matrice 1000x1000 | secvential | 20109620 ns | 0.020110 |
| Matrice 1000x1000 | 2 | 35253520 ns | 0.035254 |
| Matrice 1000x1000 | 4 | 36219740 ns | 0.036220 |
| Matrice 1000x1000 | 8 | 39355000 ns | 0.039355 |
| Matrice 1000x1000 | 16 | 42269360 ns | 0.042269 |
| Matrice 10000x10000 | secvential | 723005170 ns | 0.723005 |
| Matrice 10000x10000 | 2 | 452370520 ns | 0.452371 |
| Matrice 10000x10000 | 4 | 375744270 ns | 0.375744 |
| Matrice 10000x10000 | 8 | 317452340 ns | 0.317452 |
| Matrice 10000x10000 | 16 | 270756050 ns | 0.270756 |

---

### C++

| Tip Matrice | Nr threads | Timp executie (ns) | Timp executie (s) |
|-------------|------------|--------------------|-------------------|
| Matrice 10x10 | secvential | 4900 ns | 0.000005 |
| Matrice 10x10 | 2 | 616350 ns | 0.000616 |
| Matrice 1000x1000 | secvential | 31842760 ns | 0.031843 |
| Matrice 1000x1000 | 2 | 22542110 ns | 0.022542 |
| Matrice 1000x1000 | 4 | 15424380 ns | 0.015424 |
| Matrice 1000x1000 | 8 | 10987600 ns | 0.010988 |
| Matrice 1000x1000 | 16 | 11939920 ns | 0.011940 |
| Matrice 10000x10000 | secvential | 3065328830 ns | 3.065329 |
| Matrice 10000x10000 | 2 | 1767015770 ns | 1.767016 |
| Matrice 10000x10000 | 4 | 987240540 ns | 0.987241 |
| Matrice 10000x10000 | 8 | 810458630 ns | 0.810459 |
| Matrice 10000x10000 | 16 | 708460710 ns | 0.708461 |


---

Implementări:
- C++: thread-uri native și barieră; scriere in-place în matrice; sincronizare la fiecare „pas de rând” comun tuturor thread-urilor.
- Java: aceeași logică (3 vectori, barieră), implementată cu `CyclicBarrier` și tablouri int.

---

## Analiză: comparați performanța pentru fiecare caz

Observații per dimensiune:

- Matrice 10x10
	- Overhead-ul paralelizării domină; atât în Java cât și în C++, execuția paralelă este mai lentă decât secvențialul.

- Matrice 1000x1000
	- C++ scalează rezonabil până la 8–16 thread-uri, beneficiind de costuri mici de sincronizare.
	- Java încetinește odată cu creșterea numărului de thread-uri . Motivul este costul mare al barierei per rând și overhead JVM; la 16 thread-uri barierele devin bottleneck.

- Matrice 10000x10000
	- Ambele implementări beneficiază clar de paralelizare.
	- C++: 3.06 s → 0.71 s la 16 thread-uri (≈4.3× speedup observat, dar sub scalarea ideală din cauza memoriei/cache).
	- Java: 0.723 s → 0.271 s la 16 thread-uri (≈2.7× speedup), dar rămâne semnificativ mai lent(ă) decât C++ pentru același număr de thread-uri.

Concluzie: Paralelizarea aduce câștiguri doar pentru matrici suficient de mari; barierele per-rând impun un cost fix pe pas care penalizează Java mai mult decât C++.

---

## Compararea timpilor Java vs C++

Rezumat pe cazuri-cheie (ns, valori medii din tabele):

| Tip Matrice | Threads | Java | C++ | Raport (Java/C++) |
|-------------|---------|------|-----|--------------------|
| 1000x1000 | 1 | 20,109,620 | 31,842,760 | 0.63× (Java mai rapidă aici) |
| 1000x1000 | 2 | 35,253,520 | 22,542,110 | 1.56× |
| 1000x1000 | 4 | 36,219,740 | 15,424,380 | 2.35× |
| 1000x1000 | 8 | 39,355,000 | 10,987,600 | 3.58× |
| 1000x1000 | 16 | 42,269,360 | 11,939,920 | 3.54× |
| 10000x10000 | 1 | 723,005,170 | 3,065,328,830 | 0.24× (Java mai rapidă la 1T) |
| 10000x10000 | 2 | 452,370,520 | 1,767,015,770 | 0.26× |
| 10000x10000 | 4 | 375,744,270 | 987,240,540 | 0.38× |
| 10000x10000 | 8 | 317,452,340 | 810,458,630 | 0.39× |
| 10000x10000 | 16 | 270,756,050 | 708,460,710 | 0.38× |

Interpretare:
- La 1000x1000, C++ devine clar mai rapid pe măsură ce thread-urile cresc, datorită barierei mai ieftine și execuției native; Java plătește mai mult pe `CyclicBarrier.await()` per pas.
- La 10000x10000, Java pare mai rapidă în cifre absolute datorită acceselor de memorie în tablouri compacte, dar C++ obține totuși un speedup relativ mai mare față de propriul secvențial.

---

## Complexitate spațiu

cu 3 vectori auxiliari:

- Mască (kernel): O(k²) = O(1) pentru k fix (3)
- Per thread: 3 buffer-e de lățime m+2 → O(m) per thread
- Safe vectors între blocuri: (threads−1)×(m+2) → O(threads·m)

Total memorie: O(n·m + threads·m + k²). Ambele implementări (C++ și Java) au aceeași ordine de memorie; C++ are overhead mai redus la nivel de runtime, Java are overhead de JVM/GC, dar acesta nu afectează asimptotica.
---


Ambele implementări sincronizează „per rând global” cu o barieră. Pentru o împărțire inegală a rândurilor (ex. 1000 rânduri/16 thread-uri ⇒ 15×62 rânduri și 1×63 rânduri), toate thread-urile trebuie totuși să atingă bariera același număr de pași. O implementare corectă impune un număr egal de iterații de barieră pentru toți (ex. `maxRows`), dar costul de sincronizare rămâne mare la număr mare de thread-uri. Aceasta explică încetinirea semnificativă în Java la 16 thread-uri.

---
## Concluzii

- Paralelizarea aduce câștiguri consistente doar pentru matrici mari; pentru dimensiuni mici overhead-ul domină.
- C++ are timpi mai buni la paralelizare intensă, în timp ce Java se comportă decent dar este penalizată de costul barierei per pas.
- Complexitatea spațială este similară (O(threads * m)), cu overhead O(threads·m) pentru buffer-ele pe rând; C++ are overhead runtime mai mic.
