import type { NextConfig } from 'next';

const cors = [{ key: 'Access-Control-Allow-Origin', value: '*' }, { key: 'Cache-Control', value: 'public, max-age=300, must-revalidate' }];

const config: NextConfig = {
  // Pages read public/data from disk at request time; make sure those files ship with the functions.
  outputFileTracingIncludes: { '/*': ['./public/data/**/*'] },
  async rewrites() {
    return [
      { source: '/submit', destination: '/submit.html' },
      { source: '/gallery', destination: '/gallery.html' },
      { source: '/calendar', destination: '/calendar.html' },
      { source: '/best-practices', destination: '/docs/bounty-best-practices.html' },
      { source: '/hub', destination: '/docs/poidh-hub.html' },
      { source: '/dashboard', destination: '/docs/bounty-dashboard.html' },
      { source: '/about', destination: '/docs/about.html' },
      { source: '/lost', destination: '/docs/lost.html' },
      { source: '/create-bounty', destination: '/docs/create-bounty.html' },
      { source: '/leaderboard', destination: '/data/leaderboard.json' },
      { source: '/feedback', destination: '/feedback/index.html' },
      { source: '/feedback/:bounty', destination: '/feedback/:bounty/index.html' },
      { source: '/feedback/:bounty/:handle', destination: '/feedback/:bounty/:handle.html' },
      { source: '/round/:n', destination: '/rounds/r:n/README.md' },
      { source: '/zabal-gamez-brand', destination: '/assets/brand-kits/zabal-games/index.html' },
      { source: '/zabal-gamez-brand/:file', destination: '/assets/brand-kits/zabal-games/:file' },
    ];
  },
  async headers() {
    return [{ source: '/data/:path*', headers: cors }, { source: '/assets/brand-kits/:path*', headers: cors }];
  },
};

export default config;
