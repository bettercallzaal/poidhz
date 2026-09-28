import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// A path with a broken percent-encoding makes Next's router throw while decoding dynamic
// params, which is a 500. It is a request for nothing, so answer 404 before routing.
export function proxy(request: NextRequest) {
  try {
    decodeURIComponent(request.nextUrl.pathname);
    return NextResponse.next();
  } catch {
    return new NextResponse('Not found', { status: 404 });
  }
}

export const config = { matcher: ['/u/:path*', '/b/:path*'] };
