# Integration TODO List

## Security & Validation Issues

### DELETE Endpoint Security Vulnerabilities
- **Issue**: DELETE `/corrections/{correction_id}` accepts any UUID without verification
- **Vulnerabilities**:
  - UUID enumeration attacks (try random UUIDs to discover existing records)
  - No ownership verification (anyone with valid UUID can delete any record)  
  - No existence check before processing
  - Potential information disclosure through error responses
- **Solution Ideas**:
  - Add database existence check before deletion
  - Implement user ownership/permission validation
  - Add rate limiting for DELETE operations
  - Standardize error responses to prevent information leakage
- **Priority**: Medium (document for future security hardening)

### Data Type Safety
- **Issue**: Using `str` instead of `UUID` type for UUID parameters ✅ FIXED
- **Problem**: Accepts any string, not type-safe
- **Solution**: Use `from uuid import UUID` and proper type hints
- **Files updated**:
  - `src/api/routes/routes_corrections.py` ✅ 
  - `src/core_business_logic/correction_services.py` ✅
  - Repository layer methods
- **Priority**: Low (works but not best practice)

### UUID Exposure in URLs
- **Issue**: Full UUIDs are exposed in URL paths (e.g., `/corrections/8e600c73-8d97-40d5-927d-5ab7a94d1f8a`)
- **Security Concerns**:
  - UUIDs are visible in browser address bars, logs, and referrer headers
  - Information leakage through URL structure
  - Potential for UUID enumeration via URL monitoring
- **Solution Ideas**:
  - Use short-lived tokens or hashed identifiers for public URLs
  - Implement resource-specific access tokens
  - Add request authentication/authorization middleware
- **Priority**: Low (document for future security review)

## Current Focus
- Fix immediate DELETE 422 error by updating parameter types
- Defer security hardening to future iteration