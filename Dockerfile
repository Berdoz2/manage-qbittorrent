FROM python:3.10-alpine

# Set working directory to /app
WORKDIR /app

# Copy requirements file + make it executable
COPY --chmod=+x requirement.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy application code
COPY manage-qbittorrent.py .

# Set the command to run on container start
CMD ["python", "manage-qbittorrent.py"]