### Task-urile utilizatorilor :
 1. **Logare app** Ca si Admin si adaugare 2 user, tester si programmer
 2. **Login ca programmer** si citit descriere bug
 3. **Schimbare status bug**
 4. **Logare ca si tester** si adaugat un bug
 5. **Adaugare** 3 bug-uri in lista si **sterge** un bug din lista , dupa care adauga bug-urile in app.

---

### Utilizatori :

#### Tehnican Birou
📹 [Vizionează Video](https://github.com/redusca/Semestrul-5-Ubb/raw/main/IOC/2025-11-04_15-47-33.mp4)

#### Persoana HRs
📹 [Vizionează Video](https://github.com/redusca/Semestrul-5-Ubb/raw/main/IOC/2025-11-04_15-56-15.mp4)

---

### Feedback :
1. Aplicația pare prea simplă și lipsește ghidajul pentru utilizatorii noi  
   - Problemă: Utilizatorii noi nu înțeleg fluxurile principale (cum să raporteze un bug, cum se alocă task-urile etc.).  
   - Propuneri concrete:
     - Adăugare tutorial/flux de onboarding la primul login (modal pas-cu-pas sau tour cu evidențieri);
     - Pagina "Help" sau "Cum se folosește" cu capturi video scurte și exemple;
     - Mesaje și stări implicite mai descriptive (empty states) pe liste goale.

2. Lipsesc notificările când o acțiune reușește  
   - Problemă: Nu există feedback clar (toasts/alerts) când se creează/șterge/actualizează un bug.  
   - Propuneri concrete:
     - Implementare toasts pentru acțiuni reușite/eroare (ex: "Bug adăugat", "Schimbare status reușită");
     - Notificări persistente în UI pentru schimbări importante și atribuiri;

3. Notificarile prezente sunt agresive :
    - Problemă: Notificările prezente sunt agresive, user-ul este confuz asupra lor.
    - Propuneri concrete:
      - In loc de notificări se pot pune de exemplu in jur la field-uri, cu mesajul de eroare
      - Butoane disabled dacă user-ul nu poate continua o actiune.
