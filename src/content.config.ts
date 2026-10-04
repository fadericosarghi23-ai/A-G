import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Collection "progetti".
 * Un file .md per progetto in src/content/progetti/ (nella base: progetto-01…40 a segnaposto).
 * Le chiavi restano queste; si compilano solo i valori.
 */
const progetti = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/progetti' }),
  schema: ({ image }) =>
    z.object({
      /** Titolo del progetto, come lo chiama lo studio */
      title: z.string(),
      /** Sezione del portfolio, usata dai filtri */
      category: z.enum(['architettura', 'interior', 'allestimenti', 'concorsi']),
      /** Etichetta leggibile della sezione */
      categoryLabel: z.string(),
      /** Località; vuota se non dichiarata */
      location: z.string().default(''),
      /** Anno; vuoto se non dichiarato */
      year: z.string().default(''),
      /** Chi ha firmato il progetto */
      credits: z.string().default(''),
      /** Autore delle fotografie */
      photoCredit: z.string().default(''),
      /** Estratto usato nel mazzo in home */
      excerpt: z.string(),
      /** Paragrafi della descrizione */
      body: z.array(z.string()),
      /** Description per il <meta> della pagina di dettaglio */
      seoDescription: z.string(),
      cover: image(),
      hero: image(),
      gallery: z.array(image()).default([]),
      /** Ordine di uscita nel portfolio */
      order: z.number(),
      /** Se true compare nel mazzo della home */
      featured: z.boolean().default(false),
      /** Slug della pagina di origine sul vecchio sito, per tracciabilità */
      fonteDettaglio: z.string().default(''),
    }),
});

export const collections = { progetti };
