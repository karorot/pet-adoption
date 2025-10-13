# Pet adoption

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään ja ulos sovelluksesta.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan ilmoituksia lemmikistä, jonka haluaisi antaa adoptoitavaksi uuteen kotiin.
* Ilmoitukseen voi lisätä seuraavia tietoja:
    * Perustiedot (esim. lemmikin nimi, rotu, sukupuoli, ikä), joista osa toimii tietokantaan tallennettavien luokittelujen kautta.
    * Kuvia lemmikistä.
    * Vapaamuotoisen tekstimuotoisen kuvauksen.
* Käyttäjä pystyy näkemään ja selaamaan sovellukseen lisättyjä lemmikki-ilmoituksia ja etsimään hakusanalla.
* Käyttäjä pystyy jättämään adoptiohakemuksen toisen käyttäjän lemmikki-ilmoitukseen.
   * Lemmikin omistaja näkee kaikki lemmikilleen jätetyt hakemukset.
   * Käyttäjä näkee itse jättämänsä hakemukset.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja, kuten käyttäjän tekemät lemmikki-ilmoitukset ja jättämät hakemukset.

## Sovelluksen asennus ja testaus

Asenna flask-kirjasto:
```
$ pip install flask
```

Luo tietokannan taulut:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus:
```
$ flask run
```

## Attribution

Default pet listing image used on the front page from [Pixabay](https://pixabay.com/illustrations/pawprints-paw-prints-paw-animal-2919733/).
