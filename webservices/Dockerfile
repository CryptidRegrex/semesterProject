FROM python:3.11.9

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Step 4: Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code to the working directory
COPY . /app/

# Step 6: copy the SSL cert into the container
# COPY ssl /app/ssl

# Step 7: Expose port 8000 (the port the Django app will run on)
EXPOSE 8000

# Step 8: Set the command to run the Django server
CMD python manage.py runserver 0.0.0.0:8000 --cert-file /app/ssl/cert.pem --key-file /app/ssl/key.pem