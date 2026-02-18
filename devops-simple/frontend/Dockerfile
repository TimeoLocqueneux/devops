FROM nginx:1.27-alpine

RUN rm -rf /usr/share/nginx/html/*
COPY index.html /usr/share/nginx/html/index.html
COPY nginx-frontend.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=5 \
  CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1