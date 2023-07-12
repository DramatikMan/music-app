FROM node:alpine AS base
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1

##################
FROM base AS deps
RUN apk add --no-cache libc6-compat
COPY .npmrc package.json package-lock.json* ./
RUN npm ci

##################
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

##################
FROM base AS server
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
