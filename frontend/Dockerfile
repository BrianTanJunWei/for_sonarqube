# Use a specific Node.js version
FROM node:14

# Set the working directory and grant permissions to the new user
WORKDIR /frontend

# Copy the application code into the container
COPY . .

# Install npm dependencies
RUN npm install

# Install react-scripts globally
RUN npm install -g react-scripts

# Expose the port (for documentation)
EXPOSE 3000

# Start your React app
CMD ["npm", "start"]
