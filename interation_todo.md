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

## MinIO Dynamic Connection Resolution Analysis

### The Core Problem
MinIO container gets a new IP address every time Docker containers are restarted, but the service was using cached/hardcoded IPs, causing connection failures.

### Solution Attempts

#### Solution 1: Use Docker Service Name ❌ FAILED
**What we tried:**
- Changed connection from IP to hostname: `cover_letter_minio:9000`
- Removed `MINIO_DOMAIN` environment variable from docker-compose

**Why it failed:**
- MinIO server rejected the hostname with error: `"Invalid Request (invalid hostname)"`
- The MinIO Python client couldn't validate the hostname format

#### Solution 2: Host Network Mode ❌ FAILED  
**What we tried:**
- Added `network_mode: "host"` to service container
- Changed connection to use `localhost:9000`

**Why it failed:**
- Service on host network couldn't reach MinIO in Docker network
- They were on different network planes entirely

#### Solution 3: Fixed Docker Network Subnet ⚠️ PARTIAL SUCCESS
**What we tried:**
```yaml
networks:
  portofolio_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

**Result:**
- ✅ IPs now predictable within `172.20.x.x` range
- ❌ Still required manual IP updates due to caching issues

#### Solution 4: Dynamic IP Resolution via Startup Script ⚠️ PARTIAL SUCCESS
**What we tried:**
1. **Created startup.py** with:
   - `resolve_minio_ip()` - resolves hostname to IP using `socket.gethostbyname()`
   - `write_resolved_env()` - writes `MINIO_IP` to .env file
   - Updates `os.environ["MINIO_IP"]` for immediate effect

2. **Modified settings** to include `MINIO_IP` field

3. **Called `pre_startup()`** in main application file

**Why it partially failed:**
- ✅ Correctly resolved and wrote IP to .env
- ❌ **Pydantic BaseSettings caching** - settings instantiated once at module import
- ❌ **Singleton pattern** - `MiniOConnection._instance` cached old connection
- ❌ **Python bytecode cache** - `__pycache__` files persisted between restarts
- ❌ **Module import cache** - modules aren't re-executed on hot reload

### The Caching Problem in Detail

**Where caches existed:**
1. **Module-level**: `settings_from_env = CoverLetterSettings()` - instantiated once
2. **Singleton**: `MiniOConnection._instance` - persisted within process
3. **Python bytecode**: `__pycache__/*.pyc` files
4. **Docker volumes**: Local directory mounted, preserving cache files

**Why caches persisted:**
- `docker-compose down` doesn't delete volumes
- Hot reload (`uvicorn --reload`) doesn't clear module cache
- Pydantic loads .env once at instantiation, not on each access

### Final Working Solution ✅ (Manual)
**What works:**
1. Hardcode the current IP directly: `172.20.0.3`
2. Full nuclear rebuild when IP changes:
   - `docker-compose down -v` (removes volumes)
   - Clear `__pycache__` directories
   - Rebuild containers

### Root Causes of Failure

1. **MinIO hostname validation** - Rejects certain hostname formats
2. **Pydantic BaseSettings design** - Caches environment variables at instantiation
3. **Python module caching** - Modules imported once per process
4. **Docker networking complexity** - Different IPs for different network configurations
5. **Hot reload behavior** - Doesn't clear all caches

### What Would Actually Work (Not Implemented)

1. **Lazy loading pattern:**
   ```python
   @property
   def minio_client(self):
       # Resolve IP fresh each time
       ip = socket.gethostbyname("cover_letter_minio")
       return Minio(f"{ip}:9000", ...)
   ```

2. **Environment variable injection at container start:**
   ```yaml
   command: sh -c "export MINIO_IP=$(getent hosts cover_letter_minio | awk '{print $1}') && uvicorn ..."
   ```

3. **Service discovery tool** like Consul or custom DNS resolver

4. **Static IP assignment** in docker-compose for MinIO container

### Additional Issues Resolved

1. **PostgreSQL UUID Extension Missing**
   - Error: `function uuid_generate_v4() does not exist`
   - Solution: `CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`

2. **Duplicate Entries in SQL Seed File**
   - Error: Duplicate key violation during startup
   - Solution: Removed duplicate entry "makes me a strong candidate for this role" at line 133

3. **CORS Configuration**
   - MinIO CORS needed to be configured for browser access
   - Solution: `mc admin config set myminio api cors_allow_origin="*"`

### Key Takeaway
The fundamental issue was that every solution hit the same wall: **cached configurations that don't reload**, combined with MinIO's strict hostname validation. The manual hardcoding works but requires updates whenever Docker assigns a new IP.