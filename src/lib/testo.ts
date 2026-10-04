/**
 * I segnaposto restano nel sorgente — servono a sapere cosa manca — ma non devono
 * finire a schermo su un sito pubblicato.
 *
 * In sviluppo si vedono, così chi lavora sa dove sono i buchi.
 * In produzione spariscono: il blocco che li conteneva semplicemente non viene reso.
 */

const MARKER = /\[\[DA (COMPILARE|VALIDARE)/;

/** true se la stringa è un segnaposto e non un testo vero */
export const eSegnaposto = (s?: string | null): boolean => !!s && MARKER.test(s);

/** il testo, oppure stringa vuota in produzione se è un segnaposto */
export const testo = (s?: string | null): string => {
  if (!s) return '';
  if (!eSegnaposto(s)) return s;
  return import.meta.env.DEV ? s : '';
};

/** true se il blocco va reso (testo vero, oppure segnaposto ma siamo in sviluppo) */
export const daRendere = (s?: string | null): boolean => testo(s) !== '';

/** come testo(), ma con un ripiego quando in produzione il segnaposto sparisce */
export const testoO = (s: string | null | undefined, ripiego: string): string =>
  testo(s) || ripiego;
