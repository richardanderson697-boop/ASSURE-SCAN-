import { NextResponse } from "next/server"

// Mock database - in production, this would be your actual database
const mockScans = [
  {
    scan_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    repository_url: "https://github.com/example/secure-app",
    branch: "main",
    status: "completed",
    created_at: new Date(Date.now() - 3600000).toISOString(),
    files_scanned: 127,
    findings_count: 8,
  },
  {
    scan_id: "b2c3d4e5-f6g7-8901-bcde-fg2345678901",
    repository_url: "https://github.com/example/legacy-api",
    branch: "develop",
    status: "completed",
    created_at: new Date(Date.now() - 86400000).toISOString(),
    files_scanned: 203,
    findings_count: 23,
  },
  {
    scan_id: "c3d4e5f6-g7h8-9012-cdef-gh3456789012",
    repository_url: "https://github.com/example/mobile-app",
    branch: "main",
    status: "running",
    created_at: new Date(Date.now() - 300000).toISOString(),
    files_scanned: null,
    findings_count: null,
  },
]

export async function GET() {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 500))
  return NextResponse.json(mockScans)
}

export async function POST(request: Request) {
  const body = await request.json()

  const newScan = {
    scan_id: crypto.randomUUID(),
    repository_url: body.repository_url,
    branch: body.branch || "main",
    status: "running",
    created_at: new Date().toISOString(),
    files_scanned: null,
    findings_count: null,
    enable_ai_analysis: body.enable_ai_analysis || false,
  }

  // Add to mock database
  mockScans.unshift(newScan)

  // Simulate scan completion after 10 seconds
  setTimeout(() => {
    const scan = mockScans.find((s) => s.scan_id === newScan.scan_id)
    if (scan) {
      scan.status = "completed"
      scan.files_scanned = Math.floor(Math.random() * 200) + 50
      scan.findings_count = Math.floor(Math.random() * 30) + 5
    }
  }, 10000)

  return NextResponse.json(newScan)
}
