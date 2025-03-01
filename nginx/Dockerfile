FROM nginx:latest
# Remove the default NGINX configuration file (optional)

# Copy your custom configuration file into the container
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (optional, as NGINX already exposes it)
EXPOSE 80

# Start NGINX in the foreground
CMD ["nginx", "-g", "daemon off;"]
