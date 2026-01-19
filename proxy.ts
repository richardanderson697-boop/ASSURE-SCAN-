// For production deployment, uncomment the Auth0 version below

import { NextResponse, type NextRequest } from "next/server"

export function proxy(req: NextRequest) {
  const response = NextResponse.next()

  response.headers.set("X-Content-Type-Options", "nosniff")
  response.headers.set("X-Frame-Options", "DENY")
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin")

  return response
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|public).*)"],
}

/*
// PRODUCTION VERSION - Use this when deploying with Auth0:

import { withMiddlewareAuthRequired, getSession } from "@auth0/nextjs-auth0/edge"
import { NextResponse, type NextRequest } from "next/server"

const PUBLIC_PATHS = new Set(["/", "/api/auth/login", "/api/auth/callback", "/api/auth/logout"])

async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl

  if (
    PUBLIC_PATHS.has(pathname) ||
    pathname.startsWith("/_next") ||
    pathname.startsWith("/static") ||
    pathname.includes(".")
  ) {
    return NextResponse.next()
  }

  const session = await getSession(req, NextResponse.next())

  if (!session?.user) {
    const loginUrl = new URL("/api/auth/login", req.url)
    loginUrl.searchParams.set("returnTo", pathname)
    return NextResponse.redirect(loginUrl)
  }

  const response = NextResponse.next()
  response.headers.set("X-Content-Type-Options", "nosniff")
  response.headers.set("X-Frame-Options", "DENY")
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin")

  return response
}

export default withMiddlewareAuthRequired(middleware)

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|public|api/auth).*)"],
}
*/
