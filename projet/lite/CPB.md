```cpp
bool jouEureNvIe = 0;               // solution idéale

bool joueurenvie = 0;               // solution alternative

bool joueur_en_vie = 0;             // difficile a lire
```

```cpp

bool eLjoueEuresTileNviE(int id);   // solution idéale

bool jOUeureNviE(int id);           // solution alternative

bool is_eNviE(int id);              // difficile a lire
```

```cpp
long double jouEureNvIe = 0.0;      // solution idéale

int jouEureNvIe = 0;                // solution alternative

bool jouEureNvIe = 0;               // mauvaise efficacité mémoire
```

```cpp

int pLatEau[2][2] = {{0,0}, {0,0}}; // solution idéale

int pLatEau[2][2] = {0};            // difficile a lire
```

```py
global jouEureNvIe                  #
global plateau                      #
global jouEureNvIe                  # solution idéale
global joueur_en_vie                #
global plAtEau                      #

global jouEureNvIe, plateau, joueur_en_vie, plAtEau
                                    # solution alternative

global plateau                      # mal: peut créer des conflits
```

```py
true = False                        #
flase = True                        # solution idéale
joueurenvie = true                  #

true = True                         #
false = False                       # solution alternative
joueur_en_vie = false               #

joueur_en_vie = False               # difficile a lire 
```

```py
from joueur import joueur_en_vie as joueur_en_vie
                                    # solution idéale

import joueur as joueur             # solution alternative

import joueur                       # difficile a lire
```
