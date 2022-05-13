# Sieci Urządzeń Inteligentnych (SIU) - projekt

Repozytorium w którym znajdują się pliki należące do realizowanego przez nas projektu w ramach przedmiotu Sieci Urządzeń Inteligentnych, który polega na przygotowaniu trasy, a następnie nauczenie pojazdu poruszać się po tym torze. Do uczenia pojazdu wykorzystywane są metody sztucznej inteligencji.

## Rozpoczęcie pracy

Aby uruchomić środowisko na którym pracujemy należy mieć zainstalwane narzęcie docker oraz docker-compose

### Uruchomienie kontenera siu 
```docker-compose up -d``` (do obserwowania logów kontenera można wykorzystać ```docker-compose logs -f```)

### Uruchamianie środowiska symulacyjnego

W przeglądarce po wpisaniu adresu ```localhost:6080``` pojawi się zdalny pulpit. Po uruchomieniu zdalnego pulpitu należy uruchmoić LXTerminal i w nim wprowadzić komendę uruchamiającą środowisko symulacyjne ```roslaunch turtlesim siu.launch```

### Uruchamianie plików w kontenerze

Pliki kopiujemy do kontenera poleceniem ```./copy-to-container.sh -f {nazwa pliku}``` oraz uruchamiamy ```./run-in-container -f {nazwa pliku}```. W ramach VSCode zostały zdefiniowane dwa taski - jeden do kopiowania, drugi do kopiowania+uruchamiania pliku - wystarczy [zbindować sobie uruchamianie każdego z tych tasków](https://code.visualstudio.com/docs/editor/tasks#_binding-keyboard-shortcuts-to-tasks).

## Podmiana planszy
Nasza plansza jest zamontowana jako wolumem w kontenerze (skonfigurowane jest to w ```docker-compose.yml```)

## Napotkane błędy / problemy
* identyfikatory scenariuszy testowych należy rozpoczynać od litery

## Wykonane zmiany w plikach
