# Use an official Node.js runtime as the base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install \ 
    && npm install @mdi/font 

# Copy the rest of the application code to the container
COPY . .

# Expose the Vite development server port
EXPOSE 5173

# Start the Vue.js development server
CMD ["npm", "run", "dev", "--", "--host"]
