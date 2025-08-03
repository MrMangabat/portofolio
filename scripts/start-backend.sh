#!/bin/bash

# Backend Startup Script
# Starts all backend services locally with proper dependency management

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_COVER_LETTER_DIR="$PROJECT_ROOT/backend/services/service_cover_letter"
API_GATEWAY_DIR="$PROJECT_ROOT/backend/api_gateway"

# Log files
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"

echo -e "${BLUE}🚀 Starting Backend Services...${NC}"

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}⏳ Waiting for $service_name to be ready...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name is ready!${NC}"
            return 0
        fi
        echo -e "${YELLOW}   Attempt $attempt/$max_attempts - waiting for $service_name...${NC}"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "${RED}❌ $service_name failed to start within $((max_attempts * 2)) seconds${NC}"
    return 1
}

# Function to start databases
start_databases() {
    echo -e "${BLUE}📊 Starting database containers...${NC}"
    
    cd "$PROJECT_ROOT"
    docker-compose -f docker-compose.dev.yaml up -d
    
    echo -e "${YELLOW}⏳ Waiting for databases to be ready...${NC}"
    
    # Wait for PostgreSQL
    until docker exec postgres_dev pg_isready -U postgres >/dev/null 2>&1; do
        echo -e "${YELLOW}   Waiting for PostgreSQL...${NC}"
        sleep 2
    done
    echo -e "${GREEN}✅ PostgreSQL is ready!${NC}"
    
    # Wait for Qdrant
    until curl -s http://localhost:6333/health >/dev/null 2>&1; do
        echo -e "${YELLOW}   Waiting for Qdrant...${NC}"
        sleep 2
    done
    echo -e "${GREEN}✅ Qdrant is ready!${NC}"
    
    # Wait for MinIO
    until curl -s http://localhost:9000/minio/health/live >/dev/null 2>&1; do
        echo -e "${YELLOW}   Waiting for MinIO...${NC}"
        sleep 2
    done
    echo -e "${GREEN}✅ MinIO is ready!${NC}"
    
    echo -e "${GREEN}🎉 All databases are ready!${NC}"
}

# Function to install dependencies
install_dependencies() {
    local service_dir=$1
    local service_name=$2
    
    echo -e "${BLUE}📦 Installing dependencies for $service_name...${NC}"
    cd "$service_dir"
    
    if [ -f "pyproject.toml" ]; then
        # Use pip with pyproject.toml
        pip install -e ".[dev]" > "$LOG_DIR/${service_name}_install.log" 2>&1 || {
            echo -e "${RED}❌ Failed to install $service_name dependencies${NC}"
            echo "Check $LOG_DIR/${service_name}_install.log for details"
            return 1
        }
    elif [ -f "requirements.txt" ]; then
        # Fallback to requirements.txt
        pip install -r requirements.txt > "$LOG_DIR/${service_name}_install.log" 2>&1 || {
            echo -e "${RED}❌ Failed to install $service_name dependencies${NC}"
            return 1
        }
    elif [ -f "package.json" ]; then
        # Node.js service
        npm install > "$LOG_DIR/${service_name}_install.log" 2>&1 || {
            echo -e "${RED}❌ Failed to install $service_name dependencies${NC}"
            return 1
        }
    fi
    
    echo -e "${GREEN}✅ Dependencies installed for $service_name${NC}"
}

# Function to start a service
start_service() {
    local service_dir=$1
    local service_name=$2
    local port=$3
    local start_command=$4
    
    echo -e "${BLUE}🔧 Starting $service_name on port $port...${NC}"
    
    # Check if port is already in use
    if check_port $port; then
        echo -e "${YELLOW}⚠️  Port $port is already in use. Killing existing process...${NC}"
        pkill -f ":$port" || true
        sleep 2
    fi
    
    cd "$service_dir"
    
    # Start service in background
    eval "$start_command" > "$LOG_DIR/${service_name}.log" 2>&1 &
    local pid=$!
    echo $pid > "$LOG_DIR/${service_name}.pid"
    
    # Wait for service to be ready
    local health_url="http://localhost:$port"
    if [ "$service_name" = "service_cover_letter" ]; then
        health_url="$health_url/docs"
    elif [ "$service_name" = "api_gateway" ]; then
        health_url="$health_url/health"
    fi
    
    if wait_for_service "$health_url" "$service_name"; then
        echo -e "${GREEN}✅ $service_name started successfully (PID: $pid)${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to start $service_name${NC}"
        kill $pid 2>/dev/null || true
        return 1
    fi
}

# Cleanup function
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up...${NC}"
    
    # Kill all services
    if [ -f "$LOG_DIR/service_cover_letter.pid" ]; then
        kill $(cat "$LOG_DIR/service_cover_letter.pid") 2>/dev/null || true
        rm -f "$LOG_DIR/service_cover_letter.pid"
    fi
    
    if [ -f "$LOG_DIR/api_gateway.pid" ]; then
        kill $(cat "$LOG_DIR/api_gateway.pid") 2>/dev/null || true
        rm -f "$LOG_DIR/api_gateway.pid"
    fi
    
    echo -e "${GREEN}✅ Cleanup complete${NC}"
}

# Trap cleanup on exit
trap cleanup EXIT

# Main execution
main() {
    echo -e "${BLUE}🏗️  Backend Development Startup${NC}"
    echo -e "${BLUE}Project: Portfolio Backend Services${NC}"
    echo -e "${BLUE}Mode: Local Development${NC}"
    echo "=================================="
    
    # Start databases first
    start_databases
    
    # Install dependencies and start services
    echo -e "${BLUE}🛠️  Starting application services...${NC}"
    
    # Start Cover Letter Service
    install_dependencies "$SERVICE_COVER_LETTER_DIR" "service_cover_letter"
    start_service "$SERVICE_COVER_LETTER_DIR" "service_cover_letter" 8010 "python -m uvicorn api_cover_letter_main:app --reload --host 0.0.0.0 --port 8010"
    
    # Start API Gateway (if exists)
    if [ -d "$API_GATEWAY_DIR" ]; then
        install_dependencies "$API_GATEWAY_DIR" "api_gateway"
        start_service "$API_GATEWAY_DIR" "api_gateway" 8080 "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8080"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 All backend services are running!${NC}"
    echo "=================================="
    echo -e "${BLUE}Services:${NC}"
    echo -e "  • Cover Letter Service: ${GREEN}http://localhost:8010/docs${NC}"
    if [ -d "$API_GATEWAY_DIR" ]; then
        echo -e "  • API Gateway: ${GREEN}http://localhost:8080/docs${NC}"
    fi
    echo ""
    echo -e "${BLUE}Databases:${NC}"
    echo -e "  • PostgreSQL: ${GREEN}localhost:5432${NC}"
    echo -e "  • Qdrant: ${GREEN}http://localhost:6333${NC}"
    echo -e "  • MinIO: ${GREEN}http://localhost:9001${NC} (admin: minioadmin/minioadmin)"
    echo -e "  • Kafka: ${GREEN}localhost:9092${NC}"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
    echo -e "${BLUE}Logs are available in: $LOG_DIR${NC}"
    
    # Keep script running
    while true; do
        sleep 10
        
        # Health check - restart if any service is down
        if ! check_port 8010; then
            echo -e "${RED}❌ Cover Letter Service is down! Restarting...${NC}"
            start_service "$SERVICE_COVER_LETTER_DIR" "service_cover_letter" 8010 "python -m uvicorn api_cover_letter_main:app --reload --host 0.0.0.0 --port 8010"
        fi
        
        if [ -d "$API_GATEWAY_DIR" ] && ! check_port 8080; then
            echo -e "${RED}❌ API Gateway is down! Restarting...${NC}"
            start_service "$API_GATEWAY_DIR" "api_gateway" 8080 "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8080"
        fi
    done
}

# Help function
show_help() {
    echo "Backend Development Startup Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  --stop         Stop all running services"
    echo "  --status       Show status of all services"
    echo ""
    echo "This script will:"
    echo "  1. Start database containers (PostgreSQL, Qdrant, MinIO, Kafka)"
    echo "  2. Install Python dependencies for each service"
    echo "  3. Start all backend services with hot reload"
    echo "  4. Monitor services and restart if they crash"
}

# Handle command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    --stop)
        cleanup
        docker-compose -f docker-compose.dev.yaml down
        echo -e "${GREEN}✅ All services stopped${NC}"
        exit 0
        ;;
    --status)
        echo -e "${BLUE}Service Status:${NC}"
        check_port 8010 && echo -e "  Cover Letter Service: ${GREEN}Running${NC}" || echo -e "  Cover Letter Service: ${RED}Stopped${NC}"
        check_port 8080 && echo -e "  API Gateway: ${GREEN}Running${NC}" || echo -e "  API Gateway: ${RED}Stopped${NC}"
        exit 0
        ;;
    *)
        main
        ;;
esac