# Nuxt3 Frontend Dockerfile
FROM node:20

# Set working directory
WORKDIR /app

# Install dependencies first (for better caching)
COPY package*.json ./

# Install dependencies and rebuild native modules
RUN npm ci && npm rebuild

# Copy application code
COPY . .

# Expose port
EXPOSE 5173

# Development command with hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]