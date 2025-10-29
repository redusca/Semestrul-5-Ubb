

## Tabel rezultate

### Java

| Tip Matrice       | Nr threads  | Timp executie (ns) |
|-------------------|-------------|--------------------|
| Matrice 10x10     | secvential  | 169540             |
| Matrice 10x10     | 4        (orizontal)   | 4178620            |
| Matrice 10x10     | 4       (vertical)     | 4120050            |
| Matrice 1000x1000 | secvential  | 42570040           |
| Matrice 1000x1000 | 2        (orizontal)   | 32847250           |
| Matrice 1000x1000 | 4        (orizontal)   | 30015950           |
| Matrice 1000x1000 | 8       (orizontal)    | 30551090           |
| Matrice 1000x1000 | 16      (orizontal)    | 35191180           |
| Matrice 1000x1000 | 2     (vertical)       | 31528220           |
| Matrice 1000x1000 | 4    (vertical)        | 28582310           |
| Matrice 1000x1000 | 8    (vertical)        | 30257470           |
| Matrice 1000x1000 | 16   (vertical)        | 35442960           |
| Matrice 10x10000  | secvential  | 9695500            |
| Matrice 10x10000  | 2        (orizontal)   | 12314810           |
| Matrice 10x10000  | 4       (orizontal)    | 14115190           |
| Matrice 10x10000  | 8        (orizontal)   | 15059390           |
| Matrice 10x10000  | 16     (orizontal)     | 12899270           |
| Matrice 10x10000  | 2     (vertical)       | 12447340           |
| Matrice 10x10000  | 4    (vertical)        | 13904290           |
| Matrice 10x10000  | 8    (vertical)        | 15274360           |
| Matrice 10x10000  | 16    (vertical)       | 15345360           |
| Matrice 10000x10  | secvential  | 9323560            |
| Matrice 10000x10  | 2       (orizontal)    | 19382070           |
| Matrice 10000x10  | 4      (orizontal)     | 20903350           |
| Matrice 10000x10  | 8     (orizontal)      | 17788820           |
| Matrice 10000x10  | 16      (orizontal)    | 18095200           |
| Matrice 10000x10  | 2     (vertical)       | 15406850           |
| Matrice 10000x10  | 4     (vertical)       | 15768460           |
| Matrice 10000x10  | 8    (vertical)        | 16448360           |
| Matrice 10000x10  | 16    (vertical)       | 12903780           |
| Matrice 10000x10000 | secvential | 3620772960         |
| Matrice 10000x10000 | 2     (orizontal)     | 1906509700         |
| Matrice 10000x10000 | 4    (orizontal)      | 1070517900         |
| Matrice 10000x10000 | 8    (orizontal)      | 788225390          |
| Matrice 10000x10000 | 16   (orizontal)      | 683378090          |
| Matrice 10000x10000 | 2   (vertical)        | 2017023420         |
| Matrice 10000x10000 | 4    (vertical)       | 1099330990         |
| Matrice 10000x10000 | 8   (vertical)        | 795856150          |
| Matrice 10000x10000 | 16    (vertical)      | 687997870          |



---

### C++ Dinamic si Static

| Tip Matrice       | Tip alocare            | Nr threads   | Timp executie (ns) |
|-------------------|------------------------|---------------|--------------------|
| Matrice 10x10     | static                 | secvential    | 5510               |
| Matrice 10x10     | dynamic(orizontal)     | 4             | 665660             |
| Matrice 10x10     | dynamic(vertical)      | 4             | 630900             |
| Matrice 1000x1000 | static                 | secvential    | 130670830          |
| Matrice 1000x1000 | dynamic(orizontal)     | 2             | 64383150           |
| Matrice 1000x1000 | dynamic(orizontal)     | 4             | 34506690           |
| Matrice 1000x1000 | dynamic(orizontal)     | 8             | 29632590           |
| Matrice 1000x1000 | dynamic(orizontal)     | 16            | 28158150           |
| Matrice 1000x1000 | dynamic(vertical)      | 2             | 63786490           |
| Matrice 1000x1000 | dynamic(vertical)      | 4             | 35891090           |
| Matrice 1000x1000 | dynamic(vertical)      | 8             | 31475170           |
| Matrice 1000x1000 | dynamic(vertical)      | 16            | 28993110           |
| Matrice 10x10000  | static                 | secvential    | 12327400           |
| Matrice 10x10000  | dynamic(orizontal)     | 2             | 7091300            |
| Matrice 10x10000  | dynamic(orizontal)     | 4             | 5807240            |
| Matrice 10x10000  | dynamic(orizontal)     | 8             | 5631790            |
| Matrice 10x10000  | dynamic(orizontal)     | 16            | 13684970           |
| Matrice 10x10000  | dynamic(vertical)      | 2             | 6982170            |
| Matrice 10x10000  | dynamic(vertical)      | 4             | 4226510            |
| Matrice 10x10000  | dynamic(vertical)      | 8             | 3795400            |
| Matrice 10x10000  | dynamic(vertical)      | 16            | 3421830            |
| Matrice 10000x10  | static                 | secvential    | 12471590           |
| Matrice 10000x10  | dynamic(orizontal)     | 2             | 7750060            |
| Matrice 10000x10  | dynamic(orizontal)     | 4             | 4056780            |
| Matrice 10000x10  | dynamic(orizontal)     | 8             | 3877010            |
| Matrice 10000x10  | dynamic(orizontal)     | 16            | 4030590            |
| Matrice 10000x10  | dynamic(vertical)      | 2             | 7581940            |
| Matrice 10000x10  | dynamic(vertical)      | 4             | 6045830            |
| Matrice 10000x10  | dynamic(vertical)      | 8             | 5399830            |
| Matrice 10000x10  | dynamic(vertical)      | 16            | 14215110           |
| Matrice 10000x10000 | static               | secvential    | 12564654870        |
| Matrice 10000x10000 | dynamic(orizontal)   | 2             | 6489111240         |
| Matrice 10000x10000 | dynamic(orizontal)   | 4             | 3922012850         |
| Matrice 10000x10000 | dynamic(orizontal)   | 8             | 2394046700         |
| Matrice 10000x10000 | dynamic(orizontal)   | 16            | 2142961320         |
| Matrice 10000x10000 | dynamic(vertical)    | 2             | 7271245090         |
| Matrice 10000x10000 | dynamic(vertical)    | 4             | 4486257190         |
| Matrice 10000x10000 | dynamic(vertical)    | 8             | 2362952260         |
| Matrice 10000x10000 | dynamic(vertical)    | 16            | 2357255140         |
| Matrice 10x10     | static                 | secvential    | 26880              |
| Matrice 10x10     | static (orizontal)     | 4             | 674390             |
| Matrice 10x10     | static (vertical)      | 4             | 637950             |
| Matrice 1000x1000 | static                 | secvential    | 118124380          |
| Matrice 1000x1000 | static (orizontal)     | 2             | 59205210           |
| Matrice 1000x1000 | static (orizontal)     | 4             | 30935410           |
| Matrice 1000x1000 | static (orizontal)     | 8             | 27378120           |
| Matrice 1000x1000 | static (orizontal)     | 16            | 25513440           |
| Matrice 1000x1000 | static (vertical)      | 2             | 58496870           |
| Matrice 1000x1000 | static (vertical)      | 4             | 32980140           |
| Matrice 1000x1000 | static (vertical)      | 8             | 27129470           |
| Matrice 1000x1000 | static (vertical)      | 16            | 25890080           |
| Matrice 10x10000  | static                 | secvential    | 11398080           |
| Matrice 10x10000  | static (orizontal)     | 2             | 6645390            |
| Matrice 10x10000  | static (orizontal)     | 4             | 5492980            |
| Matrice 10x10000  | static (orizontal)     | 8             | 5367080            |
| Matrice 10x10000  | static (orizontal)     | 16            | 12553930           |
| Matrice 10x10000  | static (vertical)      | 2             | 6409310            |
| Matrice 10x10000  | static (vertical)      | 4             | 3924380            |
| Matrice 10x10000  | static (vertical)      | 8             | 3495600            |
| Matrice 10x10000  | static (vertical)      | 16            | 4209170            |
| Matrice 10000x10  | static                 | secvential    | 25030730           |
| Matrice 10000x10  | static (orizontal)     | 2             | 14599470           |
| Matrice 10000x10  | static (orizontal)     | 4             | 8881460            |
| Matrice 10000x10  | static (orizontal)     | 8             | 6463830            |
| Matrice 10000x10  | static (orizontal)     | 16            | 6496730            |
| Matrice 10000x10  | static (vertical)      | 2             | 21601430           |
| Matrice 10000x10  | static (vertical)      | 4             | 19191430           |
| Matrice 10000x10  | static (vertical)      | 8             | 24250960           |
| Matrice 10000x10  | static (vertical)      | 16            | 26462800           |
| Matrice 10000x10000 | static               | secvential    | 11389923620        |
| Matrice 10000x10000 | static (orizontal)   | 2             | 5810103880         |
| Matrice 10000x10000 | static (orizontal)   | 4             | 3093589860         |
| Matrice 10000x10000 | static (orizontal)   | 8             | 2167524650         |
| Matrice 10000x10000 | static (orizontal)   | 16            | 1986948500         |
| Matrice 10000x10000 | static (vertical)    | 2             | 5749952870         |
| Matrice 10000x10000 | static (vertical)    | 4             | 3139799450         |
| Matrice 10000x10000 | static (vertical)    | 8             | 2300307410         |
| Matrice 10000x10000 | static (vertical)    | 16            | 2047592190         |

---

- Cel mai bun timp la 10000x10000 a fost Java cu : 
| Matrice 10000x10000 | 16  (orizontal)      | 683378090          |

- C++ static a fost mai rapid decat dinamic

- **Matricea 10x10:**  
  Executia paralela cu 4 thread-uri are un timp mult mai mare decat varianta secventiala.  
  Pentru dimensiuni mici, costul crearii si sincronizarii thread-urilor depaseste beneficiul paralelizarii.

- **Matricile mari**
  Rerformanta aproape se dubleza la fiecare dublare a numarului de thread-uri, pana la saturatie.  
  Se confirma eficienta executiei paralele pentru matrici foarte alungite, unde distributia pe coloane/randuri este clara.
- **Alocare statica vs dinamica:**  
  Alocarea statica merge mai rapid decat cea dinamica pentru matricile date.

 - **Paralelizarea aduce beneficii semnificative** doar pentru dimensiuni mari ale matricei.  
   La dimensiuni reduse, overhead-ul de creare/sincronizare a thread-urilor este dominant.

 - **Implementarea C++ este in general mai performanta**, datorita:
   - gestiunii directe a memoriei,  
   - thread-urilor native,  
   - absentei JVM si a GC.

 - **Java** ofera o implementare mai stabila si scalabila pentru date mari, dar are o penalizare de initializare.

  - Cresterea numarului de thread-uri peste 8–16 aduce **diminishing returns**, datorita limitarilor hardware si ale memoriei cache.

---

## Analiza Java vs C++

| Caz | Implementare mai rapida | Observatii |
|------|--------------------------|-------------|
| Matrice 10x10 | C++ | Overhead-ul thread-urilor face Java mai lenta; C++ are apeluri native rapide. |
| Matrice 1000x1000 | C++ | De ~3× mai rapid; gestiunea memoriei si thread-urilor este mai eficienta in C++. |
| Matrice 10x10000 | Java | Performante similare sau usor mai bune la paralelizare intensa, datorita JVM optimizate. |


