# -*- coding: utf-8 -*-
"""
Genera il PDF di consegna di A+G Architettura: palette, errori corretti, miglioramenti.
Massimo quattro pagine A4, con le pastiglie di colore vere accanto ai token.

    python scripts/pdf-palette.py

Font: Garamond e Century Gothic di Windows, i più vicini a Cormorant Garamond e Jost del sito.
Il PDF viene scritto nella cartella superiore (fuori dal repository).
"""
import copy
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

FONTS = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Gara", FONTS + "GARA.TTF"))
pdfmetrics.registerFont(TTFont("GaraIt", FONTS + "GARAIT.TTF"))
pdfmetrics.registerFont(TTFont("Goth", FONTS + "GOTHIC.TTF"))
pdfmetrics.registerFont(TTFont("GothB", FONTS + "GOTHICB.TTF"))
pdfmetrics.registerFontFamily("Goth", normal="Goth", bold="GothB", italic="Goth", boldItalic="GothB")
pdfmetrics.registerFontFamily("Gara", normal="Gara", bold="Gara", italic="GaraIt", boldItalic="GaraIt")

# palette del sito (src/styles/global.css)
CIPRIA = colors.HexColor("#e5d7d6")
BG = colors.HexColor("#f3eff0")
INK = colors.HexColor("#2b2523")
MUTED = colors.HexColor("#5f5455")
LINEA = colors.HexColor("#dccdcb")
ORO = colors.HexColor("#765a31")
ORO_LOGO = colors.HexColor("#cbb280")
VERDE = colors.HexColor("#2f6b3a")

QUI = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(QUI)
LOGO = os.path.join(QUI, "_logo-wide.png")
OUT = os.path.join(os.path.dirname(ROOT), "AG-Architettura-Palette-e-Interventi.pdf")
TOTALE = [0]

# ----------------------------------------------------------------- stili
H1 = ParagraphStyle("H1", fontName="Gara", fontSize=26, leading=29, textColor=INK, alignment=TA_LEFT,
                    spaceAfter=3)
SOT = ParagraphStyle("SOT", fontName="Goth", fontSize=9.4, leading=13.6, textColor=MUTED, spaceAfter=8)
H2 = ParagraphStyle("H2", fontName="Gara", fontSize=19, leading=22, textColor=ORO, spaceBefore=9,
                    spaceAfter=4, keepWithNext=1)
P = ParagraphStyle("P", fontName="Goth", fontSize=9.2, leading=13, textColor=INK, spaceAfter=4)
PM = ParagraphStyle("PM", parent=P, textColor=MUTED, fontSize=8.8, leading=12.6)
CELL = ParagraphStyle("CELL", parent=P, fontSize=8.5, leading=11.4, spaceAfter=0)
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName="GothB")
NUM = ParagraphStyle("NUM", parent=CELL, fontName="Gara", fontSize=13, leading=13, textColor=ORO)


def cornice(c, doc):
    c.saveState()
    c.setFillColor(CIPRIA)
    c.rect(0, A4[1] - 16 * mm, A4[0], 16 * mm, stroke=0, fill=1)
    # logo originale del cliente (PNG su fondo cipria, identico alla fascia)
    c.drawImage(LOGO, 18 * mm, A4[1] - 10.6 * mm, width=52 * mm, height=52 * mm * 226 / 2203,
                mask="auto")
    c.setFont("Goth", 7.2)
    c.setFillColor(MUTED)
    c.drawRightString(A4[0] - 18 * mm, A4[1] - 9.6 * mm, "Palette, errori corretti e miglioramenti")
    c.setStrokeColor(LINEA)
    c.setLineWidth(0.5)
    c.line(18 * mm, 14 * mm, A4[0] - 18 * mm, 14 * mm)
    c.setFont("Goth", 7)
    c.drawString(18 * mm, 10 * mm, "Sito nuovo A+G Architettura · dettagli nel repository (README.md)")
    c.drawRightString(A4[0] - 18 * mm, 10 * mm,
                      "pagina %d di %d" % (doc.page, TOTALE[0]) if TOTALE[0] else "pagina %d" % doc.page)
    c.restoreState()


def tabella(dati, larghezze, extra=None):
    t = Table(dati, colWidths=larghezze, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
        ("BACKGROUND", (0, 0), (-1, 0), BG),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINEA),
    ] + (extra or [])))
    return t


def elenco(voci, primo=1):
    righe = [[Paragraph("<b>#</b>", CELL), Paragraph("<b>che cosa · come è stato corretto</b>", CELL)]]
    for i, (tit, testo) in enumerate(voci, start=primo):
        righe.append([Paragraph(str(i), NUM), Paragraph("<b>%s.</b> %s" % (tit, testo), CELL)])
    return tabella(righe, [9 * mm, 165 * mm])


story = []

# ================================================================= 1. palette
story.append(Paragraph("Palette, errori corretti e miglioramenti", H1))
story.append(Paragraph(
    "Sito nuovo di A+G Architettura (Arch. Angela Culletta, Biella · Arch. Filgena Haxhari, Vercelli), "
    "costruito sulla base architettura-studio e riempito con i contenuti di ag-architettura.it. "
    "Quattro parti: da dove viene ogni colore, che cosa è stato sbagliato e corretto, che cosa il sito "
    "nuovo fa meglio di quello attuale, e lo stato per il deploy su Netlify.", SOT))

story.append(Paragraph("1. La palette", H2))
story.append(Paragraph(
    "Tutti i colori stanno nel blocco <b>:root</b> di <b>src/styles/global.css</b>: cambiandoli lì cambia "
    "tutto il sito. Le fonti sono il logo (fondo rosa cipria, oro a gradiente <b>#c8ab78 → #9a8060</b>) "
    "e il CSS del sito attuale. I rapporti di contrasto sono calcolati con la formula WCAG.", P))

PALETTE = [
    ("--bg", "#f3eff0", "Fondo pagina", "CSS del sito attuale (fondo delle sezioni)"),
    ("--surface", "#fbf9f9", "Superfici in rilievo", "derivato da --bg"),
    ("--tint", "#e5d7d6", "Sezioni alternate, intro", "fondo del logo (rosa cipria)"),
    ("--ink", "#2b2523", "Titoli e testo forte", "bruno caldo · 13.2:1 su --bg"),
    ("--muted", "#5f5455", "Testo corrente", "6.4:1 su --bg · 5.2:1 su --tint"),
    ("--line", "#dccdcb", "Righe divisorie", "derivato dal cipria"),
    ("--line-strong", "#c4b1ae", "Bordi decisi", "derivato"),
    ("--accent", "#765a31", "Sopratitoli, bottoni, link", "oro del logo scurito · 5.6:1 su --bg"),
    ("--accent-deep", "#5c4626", "Hover dei bottoni", "derivato · 7.3:1 col bianco"),
    ("--accent-soft", "#efe6d6", "Velature leggere", "derivato"),
    ("--accent-on-dark", "#cbb280", "Accento sui fondi scuri", "oro del logo e del sito · 7.3:1"),
    ("--dark", "#2b2523", "Sezioni scure, footer", "uguale a --ink"),
    ("--dark-2", "#1f1a19", "Hover sulle sezioni scure", "derivato"),
    ("--on-dark", "#f3eff0", "Testo sulle sezioni scure", "uguale a --bg · 13.2:1"),
]
dati = [[Paragraph("<b>token</b>", CELL), "", Paragraph("<b>colore</b>", CELL),
         Paragraph("<b>ruolo</b>", CELL), Paragraph("<b>da dove viene · contrasto</b>", CELL)]]
stile = []
for i, (tok, hexv, ruolo, fonte) in enumerate(PALETTE, start=1):
    dati.append([Paragraph(tok, CELLB), "", Paragraph(hexv, CELL), Paragraph(ruolo, CELL),
                 Paragraph(fonte, CELL)])
    stile += [("BACKGROUND", (1, i), (1, i), colors.HexColor(hexv)), ("BOX", (1, i), (1, i), 0.4, LINEA)]
story.append(tabella(dati, [27 * mm, 10 * mm, 17 * mm, 45 * mm, 75 * mm], stile))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "<b>Sull'oro.</b> L'oro del logo (#cbb280) su fondo chiaro arriva a 2:1: va bene per il marchio, non "
    "per il testo. Per sopratitoli e bottoni si usa una versione scurita dello stesso oro, che supera il "
    "livello AA (4.5:1) su tutti i fondi; l'oro pieno resta dove regge, sulle sezioni scure.", PM))
story.append(Paragraph(
    "<b>Tipografia.</b> Titoli in <b>Cormorant Garamond</b>, un serif sottile ed elegante; testo in "
    "<b>Jost</b>, il sans geometrico che lo studio usa già sul sito attuale e che richiama le lettere "
    "del logo. Si cambiano in due token: --font-display e --font-body.", PM))

# ================================================================= 2. errori
story.append(Paragraph("2. Errori corretti", H2))
story.append(Paragraph(
    "Errori trovati durante il lavoro — nella base, nel riempimento o sul sito attuale — e come sono "
    "stati sistemati. Alcuni possono ripresentarsi se si rimette mano ai file: per questo sono qui.", PM))

ERRORI = [
    ("Colori di marca scritti nei componenti",
     "La base aveva un rosso chiaro (#f07575) in 10 punti, un bagliore turchese rimasto da una palette "
     "precedente e i vetri dell'header in grigio fisso: cambiando solo i token sarebbero rimasti rosso e "
     "turchese sul sito di A+G. Ora sono token (--accent-on-dark, --glow-rgb, vetri derivati da --bg)."),
    ("Oro illeggibile come testo",
     "Usare l'oro del logo per i testi piccoli dava un contrasto di 2:1. Introdotto l'oro scurito "
     "#765a31 (5.6:1) per il testo; l'oro pieno è rimasto solo sui fondi scuri."),
    ("Testo grigio di Bootstrap",
     "Il sito attuale scrive in #212529, il grigio freddo predefinito di Bootstrap, che stona col rosa e "
     "l'oro. Sostituito da un bruno caldo, #2b2523."),
    ("Residui del cliente precedente",
     "La copia della base conteneva la cartella .git di un altro studio, con la sua storia e il suo "
     "repository, e commenti che ne descrivevano il metodo. Rimossi prima di iniziare."),
    ("Didascalie segnaposto sul sito attuale",
     "Ogni galleria del sito attuale contiene \"Didascalia dell'immagine.\" ripetuto in ogni foto, "
     "residuo del template. Nel sito nuovo non c'è."),
    ("Copyright fermo al 2025",
     "Il footer attuale ha \"2020 - 2025\" scritto a mano. Ora l'anno è calcolato in automatico."),
]

ERRORI2 = [
    ("Recensione duplicata",
     "Sul sito attuale le recensioni di Emiliano A. e Samuele S. hanno lo stesso testo. Nel sito nuovo "
     "nessuna delle due compare due volte: sono state scelte 6 recensioni diverse, da validare."),
    ("Primo logo fatto a mano",
     "La prima versione del marchio era un monogramma ricostruito a mano, con il \"+\" che toccava la G. "
     "Sostituito dal ricalco vettoriale del logo vero, preso dai PNG del sito."),
    ("Foto delle due architette troppo piccole",
     "La foto insieme era di 554 px e su schermi ad alta densità risultava sgranata. Sostituita da due "
     "foto da 960 px: una in home, una nella pagina Chi siamo."),
    ("Sigla in minuscolo",
     "Il titolo dell'hero forza il minuscolo e scriveva \"a+g\". Ora la sigla resta maiuscola come nel "
     "logo; \"architettura\" resta in minuscolo."),
    ("Foto attaccata alla sezione successiva",
     "Nella pagina Chi siamo la foto toccava la fascia rosa sotto. Aggiunto lo stesso respiro che separa "
     "le altre sezioni."),
    ("Scroll bloccato dopo l'intro",
     "A fine animazione d'apertura lo scroll restava bloccato finché non scattava il timer di sicurezza. "
     "Ora si sblocca nell'istante in cui il velo esce."),
    ("Vecchi indirizzi in 404",
     "Al passaggio del dominio, link come /proj-akarui.html o /mini-call.html sarebbero finiti su una "
     "pagina d'errore, perdendo quanto indicizzato da Google. Aggiunti 17 redirect 301 nel netlify.toml."),
]
story.append(elenco(ERRORI + ERRORI2))

# ================================================================= 3. miglioramenti
story.append(Paragraph("3. Miglioramenti rispetto al sito attuale", H2))
MIGLIORIE = [
    ("Logo vettoriale",
     "Il cliente ha il logo solo in PNG. È stato ricalcato in SVG (estesa e compatta) con il gradiente "
     "oro: nitido a ogni dimensione nell'header, nella favicon e nell'immagine di condivisione."),
    ("Apertura con il logo",
     "All'ingresso i contorni oro del logo si disegnano lettera per lettera, si riempiono, un riflesso li "
     "attraversa e il velo sale. Una volta per sessione, saltabile con un clic, assente per chi riduce le "
     "animazioni."),
    ("Portfolio vero",
     "11 progetti (anche Mansarda B e Camera Gio), ognuno con pagina, galleria, luogo, anno, tipologia, "
     "servizi svolti e crediti foto, filtrabili in 4 categorie e collegati tra loro."),
    ("Servizi e prezzi chiari",
     "Le 4 pagine servizio sparse (Mini call, Chiedi ad A+G € 149, La stanza che vorrei da € 350, Casa "
     "senza pensieri) diventano un percorso in tre fasi nella pagina Metodo, e opzioni del form."),
    ("Foto ottimizzate",
     "Le immagini vengono servite in WebP alle dimensioni giuste per ogni schermo e caricate solo "
     "quando servono: pagine più leggere su mobile."),
    ("SEO e dati strutturati",
     "Titolo e descrizione per ogni pagina, dati strutturati dello studio (fondatrici, sedi, P.IVA, "
     "social), sitemap, robots.txt, canonical e Open Graph."),
    ("Accessibilità",
     "Contrasti AA su tutta la palette, link per saltare al contenuto, animazioni disattivate per chi "
     "le ha ridotte nel sistema."),
]
righe = [[Paragraph("<b>cosa</b>", CELL), Paragraph("<b>perché conta</b>", CELL)]]
for tit, testo in MIGLIORIE:
    righe.append([Paragraph("<b>%s</b>" % tit, CELL), Paragraph(testo, CELL)])
story.append(tabella(righe, [38 * mm, 136 * mm]))

# ================================================================= 4. stato
STATO = [
    ("Build", "verde: 18 pagine generate da zero, nessun errore", "ok"),
    ("Link e immagini", "1305 riferimenti interni controllati, 0 rotti", "ok"),
    ("Segnaposto", "nessuno visibile nell'HTML pubblicato", "ok"),
    ("Netlify", "netlify.toml: Node 20, install senza lockfile (fix Astro 5.18), 17 redirect 301", "ok"),
    ("Pagina privacy", "manca: il form chiede il consenso all'informativa. Testo su ag-architettura.it", "manca"),
    ("Indirizzi e orari", "il sito attuale indica solo Biella e Vercelli; la riga orari non viene resa", "manca"),
    ("Logo SVG ufficiale", "ora c'è il ricalco dal PNG: basta sostituire i file in public/brand/", "manca"),
    ("Foto in alta risoluzione", "Casa Faenza (750 px) e alcune di Casa H, L+L e Zoe sotto i 1000 px", "manca"),
    ("Form contatti", "senza endpoint apre la mail verso info@ag-architettura.it", "per scelta"),
    ("Analytics", "Google Analytics del sito attuale non portato: serve prima il banner cookie", "per scelta"),
]
righe = [[Paragraph("<b>voce</b>", CELL), Paragraph("<b>stato</b>", CELL), Paragraph("<b>esito</b>", CELL)]]
for voce, stato, esito in STATO:
    col = "#2f6b3a" if esito == "ok" else ("#5f5455" if esito == "per scelta" else "#9b2c2c")
    righe.append([Paragraph("<b>%s</b>" % voce, CELL), Paragraph(stato, CELL),
                  Paragraph('<font color="%s"><b>%s</b></font>' % (col, esito), CELL)])
story.append(KeepTogether([
    Paragraph("4. Stato per il deploy", H2),
    tabella(righe, [36 * mm, 118 * mm, 20 * mm]),
    Spacer(1, 5),
    Paragraph(
        "<b>Dominio.</b> Canonical, sitemap e Open Graph puntano già a www.ag-architettura.it. Finché il "
        "dominio mostra il sito vecchio, l'anteprima Netlify conviene proteggerla con password, per non far "
        "indicizzare due siti. <b>Form.</b> Su Netlify basta aggiungere data-netlify=\"true\" al modulo, "
        "ma dopo aver pubblicato l'informativa privacy, non prima.", PM),
]))


# ----------------------------------------------------------------- build
def costruisci(percorso, contenuto):
    d = BaseDocTemplate(percorso, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                        topMargin=22 * mm, bottomMargin=18 * mm,
                        title="A+G Architettura - palette, errori corretti e miglioramenti",
                        author="BD Media")
    f = Frame(d.leftMargin, d.bottomMargin, d.width, d.height, id="corpo")
    d.addPageTemplates([PageTemplate(id="std", frames=[f], onPage=cornice)])
    d.build(copy.deepcopy(contenuto))
    return d.page


TOTALE[0] = costruisci(os.path.join(QUI, "_conteggio.pdf"), story)
costruisci(OUT, story)
os.remove(os.path.join(QUI, "_conteggio.pdf"))
print("scritto", OUT, "-", TOTALE[0], "pagine")
