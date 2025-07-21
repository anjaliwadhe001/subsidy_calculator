# Use a minimal but compatible Debian base image
FROM debian:bullseye-slim

# Environment variables to ensure non-interactive installs
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies: Python, LaTeX, and required tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    texlive-lang-english \
    texlive-xetex \
    latexmk \
    ca-certificates \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port (if using Flask)
EXPOSE 5000

# Run the app
CMD ["python3", "subsidy_api.py"]
