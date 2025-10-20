# Descrizione progetto

Nella pagina [Il Nuovo vocabolario di base della lingua italiana](https://www.internazionale.it/opinione/tullio-de-mauro/2016/12/23/il-nuovo-vocabolario-di-base-della-lingua-italiana) si può trovare il file PDF con l’elenco alfabetico dei vocaboli del «Nuovo vocabolario di base della lingua italiana» comprensivo anche delle loro qualifiche grammaticali e marche d’uso (vedasi anche [Avvertenze per la consultazione del «Nuovo De Mauro»](https://dizionario.internazionale.it/avvertenze/)).

Dato che sarebbe molto interessante fare un’analisi statistica sulla distribuzione dei vari tipi di vocaboli, si presenta un *parser* per trasformare il file PDF in un file JSON così da rendere i dati fruibili per analisi automatizzate. 

## Utilizzo del parser

Sono necessari:

- [Python](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv)

Lanciando il comando
```
uv sync & uv run scripts/parser.py
```
verrà creato il file `vocabolario.json` nella directory `output`.

## Osservazioni e statistiche

Dall’analisi del file JSON generato dal parser si possono notare alcune cose interessanti. 

- I seguenti lemmi appaiono due volte nel file PDF:

  - «arrendersi», prima in tondo chiaro e subito dopo in corsivo chiaro (nel file JSON è indicato come «parola di alta disponibilità»);
  - «madrileno», appare due volte consecutive in corsivo chiaro (nel file JSON è indicato come «parola di alta disponibilità»);
  - «migliaio», prima in corsivo chiaro e subito dopo in neretto tondo (nel file JSON è indicato come «parola fondamentale»);
  - «sé», appare prima in tondo chiaro e poi in neretto tondo (nel file JSON è indicato come «parola fondamentale»).

- È presente un solo lemma polirematico, ovvero «TG sigla».
- È presente un solo lemma senza qualifica grammaticale, ovvero «TG sigla» (cioè il solo lemma polirematico).

In totale sono presenti 7245 lemmi, così suddivisi in base alla marca d’uso:
- numero di lemmi con marca d’uso «parola fondamentale»: 2002;
- numero di lemmi con marca d’uso «parola di alta disponibilità»: 2230;
- numero di lemmi con marca d’uso «parola di alto uso»: 3013.

## Esempi di analisi

Nel vocabolario ci sono 856 lemmi *sostantivi maschili* con marca d’uso «parola fondamentale».

Nel vocabolario ci sono 447 lemmi che sono *verbi sia transitivi che intransitivi*.

C’è un unico verbo pronominale che è sia transitivo che intransitivo, ovvero «riconciliarsi».
