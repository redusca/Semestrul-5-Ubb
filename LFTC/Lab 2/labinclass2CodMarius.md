Automat
    stari : List<Stare>
    alfabet : Set<String>
    tranzitii : MultiMap<Tuple < Stare ,Stare >,String>
    stare_initiala : Stare
    stari_finale : List<Stare>

Stare // ex : q0 , a2
    Eticheta : String // ex : q , a, b ,c
    Index : Number // ex : 0 , 1 ,2 3,