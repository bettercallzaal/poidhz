import handler from '@/legacy-api/claim-meta.mjs';
export const runtime = 'edge';
export const GET = (req: Request) => handler(req);
