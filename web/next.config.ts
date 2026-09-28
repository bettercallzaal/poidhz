import type { NextConfig } from 'next';

const cors = [{ key: 'Access-Control-Allow-Origin', value: '*' }, { key: 'Cache-Control', value: 'public, max-age=300, must-revalidate' }];

const config: NextConfig = {
  // Pages read public/data from disk at request time; make sure those files ship with the functions.
  outputFileTracingIncludes: { '/*': ['./public/data/**/*'] },
  async redirects() {
    return [
      { source: '/index.html', destination: '/', permanent: false },
      { source: '/people.html', destination: '/people', permanent: false },
    ];
  },
  async rewrites() {
    const afterFiles = [
      { source: '/best-practices', destination: '/docs/bounty-best-practices' },
      { source: '/hub', destination: '/docs/poidh-hub' },
      { source: '/dashboard', destination: '/docs/bounty-dashboard' },
      { source: '/about', destination: '/docs/about' },
      { source: '/lost', destination: '/docs/lost' },
      { source: '/create-bounty', destination: '/docs/create-bounty' },
      { source: '/leaderboard', destination: '/data/leaderboard.json' },
      { source: '/feedback', destination: '/feedback/index.html' },
      { source: '/feedback/:bounty', destination: '/feedback/:bounty/index.html' },
      { source: '/feedback/:bounty/:handle', destination: '/feedback/:bounty/:handle' },
      { source: '/round/:n', destination: '/rounds/r:n/README.md' },
      { source: '/round/:n/judging', destination: '/rounds/r:n/judging' },
      { source: '/zabal-gamez-brand', destination: '/assets/brand-kits/zabal-games/index' },
      { source: '/zabal-gamez-brand/:file', destination: '/assets/brand-kits/zabal-games/:file' },
    ];
    // The old site had cleanUrls: any file.html was reachable without its extension. Vercel serves
    // public HTML at the clean path in production, so rewrites above target clean paths and this
    // fallback supplies the .html only where a server (next start) needs it.
    const fallback = [{ source: '/:path*', destination: '/:path*.html' }];
    return { beforeFiles: [], afterFiles, fallback };
  },
  async headers() {
    return [{ source: '/data/:path*', headers: cors }, { source: '/assets/brand-kits/:path*', headers: cors }];
  },
};

export default config;
