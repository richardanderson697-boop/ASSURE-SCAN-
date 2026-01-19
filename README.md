# Code Compliance Scanner - Production Setup

Enterprise-grade code security and compliance scanning platform with Auth0 authentication and FastAPI backend.

## Architecture

### Frontend (Next.js 16)
- **Framework**: Next.js 16 with App Router
- **Authentication**: Auth0 (RBAC with org_admin, developer, auditor roles)
- **UI Components**: Radix UI + Tailwind CSS
- **Real-time Updates**: Polling-based scan status updates

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11+
- **Database**: SQLAlchemy with PostgreSQL
- **Security**: JWT validation, JWKS caching, RBAC middleware
- **Scanning**: Hybrid pattern-based + AI-powered (Claude) analysis
- **Events**: Kafka for event-driven architecture
- **Compliance**: SOC 2, GDPR, OWASP Top 10, ISO 27001, PCI DSS

## Environment Variables

Create a `.env.local` file in the root directory:

```bash
# Auth0 Configuration
AUTH0_SECRET='your-auth0-secret-here'
AUTH0_BASE_URL='http://localhost:3000'
AUTH0_ISSUER_BASE_URL='https://your-tenant.auth0.com'
AUTH0_CLIENT_ID='your-client-id'
AUTH0_CLIENT_SECRET='your-client-secret'
AUTH0_NAMESPACE='https://your-app.com'
NEXT_PUBLIC_AUTH0_NAMESPACE='https://your-app.com'

# API Configuration
NEXT_PUBLIC_API_URL='http://localhost:8000'
```

### Auth0 Setup

1. **Create Auth0 Application**:
   - Go to Auth0 Dashboard → Applications → Create Application
   - Choose "Regular Web Application"
   - Note your Domain, Client ID, and Client Secret

2. **Configure Callback URLs**:
   - Allowed Callback URLs: `http://localhost:3000/api/auth/callback`
   - Allowed Logout URLs: `http://localhost:3000`
   - Allowed Web Origins: `http://localhost:3000`

3. **Add Custom Claims (Action)**:
   Create an Auth0 Action to add custom claims:
   ```javascript
   exports.onExecutePostLogin = async (event, api) => {
     const namespace = 'https://your-app.com';
     
     // Add roles from user metadata or app metadata
     if (event.authorization) {
       api.idToken.setCustomClaim(`${namespace}roles`, event.authorization.roles || []);
       api.accessToken.setCustomClaim(`${namespace}roles`, event.authorization.roles || []);
     }
     
     // Add organization ID
     if (event.user.app_metadata?.organization_id) {
       api.idToken.setCustomClaim(`${namespace}organization_id`, event.user.app_metadata.organization_id);
       api.accessToken.setCustomClaim(`${namespace}organization_id`, event.user.app_metadata.organization_id);
     }
   };
   ```

4. **Set User Roles**:
   - Go to User Management → Users → Select User
   - Edit app_metadata:
   ```json
   {
     "roles": ["org_admin"],
     "organization_id": "org-123"
   }
   ```

## Backend Setup (FastAPI)

Your FastAPI backend files are ready. Set up the backend:

1. **Install Dependencies**:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose[cryptography] requests anthropic kafka-python
```

2. **Environment Variables** (`.env`):
```bash
# Database
DATABASE_URL='postgresql://user:password@localhost:5432/codescan'

# Auth0
AUTH0_DOMAIN='your-tenant.auth0.com'
AUTH0_AUDIENCE='https://your-api.com'
AUTH0_NAMESPACE='https://your-app.com'

# GitHub Access
GITHUB_TOKEN='your-github-token'

# AI Analysis (Claude)
ANTHROPIC_API_KEY='your-anthropic-key'

# Kafka (optional)
KAFKA_BOOTSTRAP_SERVERS='localhost:9092'
```

3. **Run Database Migrations**:
```bash
# Create tables from your SQLAlchemy models
python -m scripts.init_db
```

4. **Start FastAPI Server**:
```bash
uvicorn main:app --reload --port 8000
```

## Development

### Start Next.js Frontend:
```bash
npm install
npm run dev
```

Access the app at `http://localhost:3000`

### Test Real Scanning:

1. Sign in with Auth0
2. Click "New Scan"
3. Enter a GitHub repository URL (e.g., `https://github.com/your-org/your-repo`)
4. Select branch and enable AI analysis
5. Click "Start Scan"

The scan will:
- Clone the repository
- Run pattern-based security checks (SQL injection, XSS, secrets, etc.)
- Execute AI-powered deep analysis (if enabled)
- Calculate compliance scores
- Display findings in real-time

## Deployment

### Deploy to Vercel (Frontend):
```bash
vercel deploy
```

Add environment variables in Vercel dashboard.

### Deploy Backend:
- **Railway**: Connect GitHub repo, set environment variables
- **AWS ECS/Fargate**: Containerize with Docker
- **Google Cloud Run**: Deploy as container
- **DigitalOcean App Platform**: Connect GitHub repo

### Production Checklist:
- [ ] Configure Auth0 production credentials
- [ ] Set up PostgreSQL database
- [ ] Configure Kafka (if using events)
- [ ] Add GitHub token with repo access
- [ ] Set Anthropic API key for AI scanning
- [ ] Update CORS settings in FastAPI
- [ ] Enable HTTPS
- [ ] Set up monitoring (Sentry, DataDog)
- [ ] Configure rate limiting
- [ ] Set up backups

## API Endpoints

### Scans:
- `POST /api/v1/scans` - Create new scan
- `GET /api/v1/scans` - List scans
- `GET /api/v1/scans/{scan_id}` - Get scan results
- `GET /api/v1/scans/{scan_id}/status` - Get scan status

### Organizations:
- `GET /api/v1/organizations/{org_id}/scans` - Get org scans
- `GET /api/v1/organizations/{org_id}/audit-logs` - Get audit logs

## Security Features

- **Authentication**: Auth0 with JWT validation
- **Authorization**: Role-based access control (RBAC)
- **Audit Logging**: All actions logged for compliance
- **Data Isolation**: Multi-tenant with organization-level isolation
- **GDPR Compliance**: Right to be forgotten, data encryption
- **Security Headers**: CSP, HSTS, X-Frame-Options

## Support

For issues or questions:
1. Check logs in FastAPI (`uvicorn` output)
2. Check browser console for frontend errors
3. Verify Auth0 configuration
4. Ensure backend is running and accessible

## License

Proprietary - All rights reserved
