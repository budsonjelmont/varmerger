FROM nginx:alpine

ARG CONTEXTPATH=/app/nginx

RUN rm /etc/nginx/nginx.conf
COPY ${CONTEXTPATH}/nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY ${CONTEXTPATH}/project.conf /etc/nginx/conf.d/
