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

# Expose Vite default port
EXPOSE 5173

# Start Vite in dev mode, watching for file changes
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]