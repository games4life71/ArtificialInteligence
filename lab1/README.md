# Modelarea unei probleme de decizie

1. Pentru modelarea starii am folosit o matrice care indica pozitiile numerelor dar si a spatiului liber cat si vecinii acestora plus un string care arata care a fost ultima mutare (up, down, left, right).
2. Functia *transform_input* primeste ca parametri instanta problemei si intoarce starea initiala, iar *check_final_state* verifica daca starea curenta este una finala.
3. Functia *possible_moves* arata toate posibilele mutari pe care le pot face in functie de unde se afla pozitionata casuta libera; *check_legal_move* verfica daca mutarea este valida si daca ultima mutare facuta si cea din pasul curent sunt diferite (daca am mutat casuta libera sus, apoi o mutam iar jos nu e corect) pentru regula >După mutarea unei celule, ea nu mai poate fi mutată din nou decât după ce unul din vecinii săi a fost mutat; *transition_move* se foloseste de functia anterioara pentru a muta efectiv celula.
4. Functiile *IDDFS* si *depth_limited_DFS* implementeaza algoritmul **IDDFS** (Iterative Deepening Depth First Search).
