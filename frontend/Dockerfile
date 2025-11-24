FROM node:18-alpine

WORKDIR /app

# Copy dependencies
COPY frontend/package*.json ./

# Install dependencies with cache for node_modules
RUN npm install --legacy-peer-deps && npm cache clean --force

# Copy application
COPY frontend/ ./

EXPOSE 3000

CMD ["npm", "run", "dev"]
