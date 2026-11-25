FROM node:24-bookworm-slim AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY nuxt.config.ts tsconfig.json ./
COPY app ./app
COPY public ./public
RUN npm run generate

FROM nginx@sha256:583b7f2fce1cdb8da5ad5c39ebd3c33b98b87d493190e548bdee1fa8c619c311
COPY --from=build /app/.output/public /usr/share/nginx/html
