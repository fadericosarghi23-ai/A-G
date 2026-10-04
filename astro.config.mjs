import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Dominio canonico del sito: segnaposto della base, sostituire con quello del cliente.
export const SITE_URL = 'https://www.ag-architettura.it';

export default defineConfig({
  site: SITE_URL,
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap()],
});
