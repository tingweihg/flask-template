
# Use the Nginx image
FROM nginx

# Replace with our own nginx.conf
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
 
# ssl csr and key
COPY nginx/ssl.csr /etc/nginx/cert/ssl.csr
COPY nginx/ssl.key /etc/nginx/cert/ssl.key
