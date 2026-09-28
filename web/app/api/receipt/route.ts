import handler from '@/legacy-api/receipt.mjs';
export const runtime = 'edge';
export const GET = (req: Request) => handler(req);
