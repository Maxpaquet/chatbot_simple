FROM node:18-alpine
WORKDIR /app

# Copier les fichiers nécessaires
COPY package.json package-lock.json* ./

# Installer les dépendances (dev + prod)
RUN if [ -f package-lock.json ]; then npm ci --silent; else npm install --silent; fi

# Copier tout le code
COPY . .

# Build Next.js
RUN npm run build

# Exposer le port et lancer Next.js
EXPOSE 3000
CMD ["npm", "run", "start"]


# # Build stage
# FROM node:18-alpine AS builder
# WORKDIR /app



# # On copie package.json + package-lock.json
# COPY package.json package-lock.json* ./

# # Install avec lockfile si dispo
# RUN if [ -f package-lock.json ]; then npm ci --silent; else npm install --silent; fi

# COPY . .
# RUN npm run build

# # Runner
# FROM node:18-alpine AS runner
# WORKDIR /app
# ENV NODE_ENV=production

# COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/node_modules ./node_modules
# COPY --from=builder /app/package.json ./package.json
# COPY --from=builder /app/public ./public

# EXPOSE 3000
# CMD ["npm", "run", "start"]