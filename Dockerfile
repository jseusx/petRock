FROM nginx:alpine

# Copy the entire frontend folder into NGINX's default directory

# Copy HTML files from the frontend/html folder into the container's web root
COPY frontend/html/ /usr/share/nginx/html/

# Copy CSS files from frontend/css folder
COPY frontend/css/ /usr/share/nginx/html/css/

# Copy JS files from the frontend/js folder
COPY frontend/js/  /usr/share/nginx/html/js/

COPY frontend/src/ usr/share/nginx/html/src/

# Expose port 80 so that the container can accept HTTP traffic
EXPOSE 80