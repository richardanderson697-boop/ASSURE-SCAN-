"use client"

// For production, uncomment the Auth0 implementation below

export type UserRole = "org_admin" | "developer" | "auditor"

export function useUserRoles(): string[] {
  return []
}

export function useHasRole(...roles: string[]): boolean {
  return false
}

export function useOrganizationId(): string | null {
  return null
}

export function useUserContext() {
  return {
    user: null,
    isLoading: false,
    error: null,
    roles: [],
    organizationId: null,
    isAuthenticated: false,
  }
}

/*
// PRODUCTION VERSION - Use this when deploying with Auth0:

import { useUser } from "@auth0/nextjs-auth0/client"

export type UserRole = "org_admin" | "developer" | "auditor"

export function useUserRoles(): string[] {
  const { user } = useUser()
  if (!user) return []
  const namespace = process.env.NEXT_PUBLIC_AUTH0_NAMESPACE!
  return (user[`${namespace}roles`] as string[]) ?? []
}

export function useHasRole(...roles: string[]): boolean {
  const userRoles = useUserRoles()
  return roles.some((role) => userRoles.includes(role))
}

export function useOrganizationId(): string | null {
  const { user } = useUser()
  if (!user) return null
  const namespace = process.env.NEXT_PUBLIC_AUTH0_NAMESPACE!
  return user[`${namespace}organization_id`] as string | null
}

export function useUserContext() {
  const { user, isLoading, error } = useUser()
  const roles = useUserRoles()
  const organizationId = useOrganizationId()

  return {
    user,
    isLoading,
    error,
    roles,
    organizationId,
    isAuthenticated: !!user,
  }
}
*/
