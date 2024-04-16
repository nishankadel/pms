FROM python:3.8-slim

# Set the working directory in the container
WORKDIR C:\Users\kcani\Desktop\pythongroupproject\pms


# Copy the current directory contents into the container
COPY . .
 

# (Optional) Expose port 80 if your app is a web application
EXPOSE 80

# Run your application
CMD ["python", "./run.py"]