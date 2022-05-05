# Sieci Urządzeń Inteligentnych (SIU) - projekt

Repozytorium w którym znajdują się pliki należące do realizowanego przez nas projektu w ramach przedmiotu Sieci Urządzeń Inteligentnych, który polega na przygotowaniu trasy, a następnie nauczenie pojazdu poruszać się po tym torze. Do uczenia pojazdu wykorzystywane są metody sztucznej inteligencji.

## Rozpoczęcie pracy

Aby uruchomić środowisko na którym pracujemy należy mieć zainstalwane narzęcie docker
Po wpisaniu polecenia (może być wymagane dodanie ```sudo```):
```
docker run -p 6080:80 dudekw/siu-base
```
w przeglądarce po wpisaniu adresu ```localhost:6080``` pojawi się zdalny pulpit.

Po uruchomieniu zdalnego pulpitu należy uruchmoić LXTerminal i w nim wprowadzić komendę 
```
roslaunch turtlesim siu.launch
```

## Podmiana planszy
Aby zmienić planszę na stworzony przez nas tor należy w dockerze zmienić plik roads.png na stworzony przez nas plik board.png

## Wykonane zmiany w plikach
