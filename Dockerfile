# Use nginx alpine image for a lightweight container
FROM nginx:alpine

# Copy all HTML, CSS, JS, and image files to nginx's default web directory
COPY . /usr/share/nginx/html

# Expose port 80 for web traffic
EXPOSE 80

# Start nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
