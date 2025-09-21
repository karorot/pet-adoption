# Pet adoption

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään ja ulos sovelluksesta.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan ilmoituksia lemmikistä, jonka haluaisi antaa adoptoitavaksi uuteen kotiin.
* Ilmoitukseen voi lisätä seuraavia tietoja:
    * Perustiedot (esim. lemmikin nimi, rotu, sukupuoli, sijainti).
    * Erilaisia luokitteluja (esim. sopii lapsiperheeseen, ongelmakäytöstä, terveydentila).
    * Kuvia lemmikistä.
    * Vapaamuotoisen tekstimuotoisen kuvauksen.
* Käyttäjä pystyy näkemään ja selaamaan sovellukseen lisättyjä lemmikki-ilmoituksia ja etsimään hakusanalla.
* Käyttäjä pystyy jättämään adoptiohakemuksen ilmoitukseen.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja, käyttäjän tekemät ilmoitukset ja jättämät hakemukset.

## Sovelluksen asennus ja testaus

Asenna flask-kirjasto:
```
$ pip install flask
```

Luo tietokannan taulut:
```
$ sqlite3 database.db < schema.sql
```

Käynnistä sovellus:
```
$ flask run
```
