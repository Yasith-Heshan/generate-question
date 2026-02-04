# Use official Node.js image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the app
COPY . .

# Expose Vite port
EXPOSE 5174

# Start Vite in dev mode, watching for file changes
RUN ["npm", "run", "dev"]