# Dependency stage
FROM node:24-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --ignore-scripts

# Build stage
FROM node:24-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ARG NEXT_PUBLIC_API_URL=http://localhost:8000/api
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
# Cap Next.js build heap so low-RAM VPS stays responsive (SSH/web) during builds
ENV NODE_OPTIONS=--max-old-space-size=1536
RUN npm run build

# Runner stage (standalone)
FROM node:24-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./.next/static
COPY --from=build /app/public ./public
COPY --from=build /app/messages ./messages
COPY --from=build /app/i18n ./i18n
EXPOSE 3000
CMD ["node", "server.js"]