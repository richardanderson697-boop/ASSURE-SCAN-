// Real API client that connects to your FastAPI backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080"

async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    credentials: "include",
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Request failed" }))
    throw new Error(error.error || error.detail || "API request failed")
  }

  return response.json()
}

export const api = {
  async createScan(data: {
    repository_url: string
    branch: string
    enable_ai_analysis: boolean
  }) {
    return fetchAPI("/api/v1/scans", {
      method: "POST",
      body: JSON.stringify(data),
    })
  },

  async getScans() {
    return fetchAPI("/api/v1/scans")
  },

  async getScanStatus(scanId: string) {
    return fetchAPI(`/api/v1/scans/${scanId}/status`)
  },

  async getScanResults(scanId: string) {
    return fetchAPI(`/api/v1/scans/${scanId}`)
  },

  async getOrganizationScans(orgId: string) {
    return fetchAPI(`/api/v1/organizations/${orgId}/scans`)
  },
}
