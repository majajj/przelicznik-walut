#### Autor: ...

- `example_currency_rates.json` - lokalne źródło danych z kursami walut
- `database.json` - baza danych z zapisanymi kursami walut

Program uruchamiamy podając zestaw argumentów:
1) dev lub prod
2) plik lub nbp
3) waluta np EUR
4) price 
przykład uruchomienia poniżej:

 python -m task dev plik EUR 220   
 
testy napisane w pyteście uruchamiamy komendą pytest
db_prod -> baza sqllite produkcyjna
db_for_test -> baza do wykonywania testów