FROM continuumio/miniconda3:24.1.2-0

WORKDIR /app

# Add necessary files
ADD ./scripts/run-dev.sh /app/scripts/run-dev.sh
ADD ./requirements.txt /app/requirements.txt

# Install build tools and dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    gcc \
    make \
    automake \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Run setup script
RUN bash ./scripts/run-dev.sh

# Install Python dependencies
RUN pip install -r requirements.txt

# Add the rest of the application files
ADD ./ /app

# Command to run the application
CMD ["bash", "scripts/run-dev.sh"]