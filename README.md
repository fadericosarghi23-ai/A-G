# A+G Architettura — sito

Studio di architettura e interior design di Arch. Angela Culletta (Biella) e Arch. Filgena Haxhari
(Vercelli). Clone di `base-architettura-studio-3` riempito con la mappa
`mappa-riempimento-ag-architettura.md` e con i contenuti del sito attuale ag-architettura.it.

Astro 5 + content collections, CSS vanilla, font Cormorant Garamond (titoli) + Jost (testo).

```
npm run dev      # http://localhost:4690
npm run build    # dist/ (18 pagine)
npm run slots    # conta [[DA COMPILARE]] e [[DA VALIDARE]] rimasti
```

## Cosa c'è

- **Pagine**: home, progetti (elenco + 11 schede), servizi (`/ambiti/`), metodo, chi siamo (`/studio/`),
  contatti, 404.
- **Progetti**: gli 11 lavori del sito attuale, inclusi Mansarda B e Camera Gio (sul sito ma non nella
  mappa). Hanno testi, luogo, anno, tipologia, servizi svolti e crediti foto presi parola per parola
  dalle pagine `proj-*.html`. 149 foto in `src/assets/progetti/<slug>/`. Le foto "prima" di Mansarda B
  e Camera Gio (4 in tutto) sono escluse dalla galleria.
- **Categorie** (le chiavi della base restano, cambiano i nomi): Ristrutturazioni (6), Interni su misura (3),
  Singoli ambienti (1), Retail (1).
- **Servizi** del sito attuale (Mini call gratuita, Chiedi ad A+G € 149, La stanza che vorrei da € 350,
  Casa senza pensieri su misura): stanno nelle card della pagina Metodo e tra le opzioni del form.
- **Recensioni**: 6 delle 14 del sito, nella griglia della pagina Chi siamo. La base non ha una sezione
  recensioni.
- **Team**: le due architette, con le bio originali e i ritratti del sito (490 px).

## Palette (solo token, `src/styles/global.css`)

Presa dal logo (fondo rosa cipria `#e5d7d6`, oro a gradiente `#c8ab78 → #9a8060`) e dal CSS del sito
(`#f3eff0`, `#cbb280`).

| Token | Valore | Note |
| --- | --- | --- |
| `--bg` | `#f3eff0` | fondo sezioni del sito attuale |
| `--tint` | `#e5d7d6` | rosa cipria del logo |
| `--ink` | `#2b2523` | bruno caldo (il `#212529` del sito era il default di Bootstrap) |
| `--muted` | `#5f5455` | 6.4:1 su `--bg`, 5.2:1 su `--tint` |
| `--accent` | `#765a31` | oro del logo scurito: 5.6:1 su `--bg`, 4.6:1 su `--tint`, 6.4:1 col bianco |
| `--accent-on-dark` | `#cbb280` | oro pieno del logo, sui fondali scuri (7.3:1) |
| `--dark` / `--dark-2` | `#2b2523` / `#1f1a19` | fondali scuri |

Font: Cormorant Garamond per i titoli (serif elegante, scelto su richiesta) e Jost per il testo, il sans
geometrico che lo studio usa già sul sito attuale. Si cambiano solo in `--font-display` / `--font-body`.

## Marchio

Il cliente ha solo PNG. `public/brand/logo.svg` (esteso, nell'header e nel menu mobile) e
`logo-compatto.svg` sono il **loro logo ricalcato in vettoriale** dai PNG del sito (`ag_logo_wide.png`,
`ag_logo_narrow.png`), con il gradiente oro. `favicon.svg` e `mark.svg` sono il logo compatto su fondo
cipria. `favicon-32.png` e `apple-touch-icon.png` sono le loro icone originali. `og-cover.jpg` è il logo
esteso originale su fondo cipria. Quando arriva l'SVG ufficiale basta sostituire i file.

## Foto e video

- Foto: 149 dei progetti, più ritratti e 2 foto di Angela e Ghena insieme (home: sul divano; Chi siamo:
  alla scrivania). Sono tutte quelle del sito con un posto nel layout.
- Non inserite, perché la base non ha uno spazio adatto: `minicall.jpeg`, 2 foto di cantiere in home,
  i 24 riquadri del feed Instagram (moodboard, book di progetto, dettagli).
- Video: il sito attuale non ne ha. Ci sono solo link a 23 post Instagram.

## Aperti — `[[DA COMPILARE]]` (manca il dato)

1. Indirizzi civici e CAP delle due sedi: footer, card contatti, JSON-LD (senza `geo`).
2. Orari di ricevimento: footer e contatti. In produzione la riga non viene resa.
3. Ritratti del team in alta risoluzione (oggi 490 px).

## Da validare col cliente — `[[DA VALIDARE]]` (testi scritti da noi)

Nomi e sintesi delle 4 categorie (home + servizi); titoli delle fasi del metodo e sintesi delle card;
scelta delle 6 recensioni con le etichette del tipo di lavoro; introduzione all'elenco progetti;
tempistiche del form e testo del consenso privacy.

## Prima di pubblicare

- **Pagina privacy/cookie**: la base non la prevede, ma il form chiede il consenso all'informativa e la
  mappa la vuole linkata nel footer. Il testo è su ag-architettura.it/privacy.html
  (titolare Arch. Angela Culletta, P.IVA 06368110828).
- **Form**: `data-endpoint=""`. Finché non c'è un endpoint (Formspree/Resend/Netlify Forms), il modulo apre
  il client di posta verso info@ag-architettura.it (`FALLBACK_EMAIL`).
- **Analytics**: il sito attuale ha Google Analytics `G-J7T4ZSTQ7K`. Non è stato portato: serve prima
  un banner cookie.
- Foto basse: Casa Faenza (5 verticali 750×1000, anche come hero a tutto schermo) e alcune di Casa H,
  Casa L+L e Zoe sotto i 1000 px. Meglio averle dal cliente in alta risoluzione.
- Deploy su Netlify: `netlify.toml` ha già il fix di Astro 5.18 (Node 20, lockfile non versionato).

## Deploy e consegna

- `netlify.toml` contiene anche **17 redirect 301** dai vecchi indirizzi (`/proj-*.html`, `/progetti.html`,
  pagine servizio) alle pagine nuove: servono quando il dominio passa al sito nuovo.
- Intro all'apertura (`src/components/IntroOverlay.astro`): il logo compatto si disegna e si riempie d'oro,
  poi il velo sale. Una volta per sessione; legge il tracciato da `public/brand/logo-compatto.svg`.
- Report per il cliente (palette, errori corretti, miglioramenti): `python scripts/pdf-palette.py`
  scrive `AG-Architettura-Palette-e-Interventi.pdf` nella cartella superiore.
