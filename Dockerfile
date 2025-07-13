# Use a minimal Debian image
FROM debian:bullseye-slim

# Install Python, LaTeX, pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port (optional, for clarity)
EXPOSE 5000

# Run your Flask app
CMD ["python3", "subsidy_api.py"]
