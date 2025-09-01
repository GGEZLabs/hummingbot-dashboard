# =================================================================
# STAGE 1: Builder
# Builds Python 3.12-compatible wheels in a consistent environment.
# =================================================================
FROM continuumio/miniconda3:latest AS builder

# Install essential build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Create the final Dashboard environment from its YAML file.
COPY hummingbot-dashboard/environment_conda.yml .
RUN conda env create -f environment_conda.yml

# 2. Install build dependencies inside the environment
RUN conda run -n dashboard pip install --no-cache-dir cython "numpy<2.0.0" wheel setuptools build

# 3. Copy sources
COPY hummingbot ./hummingbot-source
COPY hummingbot-api-client ./hummingbot-api-client

# 4. Build the hummingbot wheel (setup.py-based)
WORKDIR /app/hummingbot-source
RUN conda run -n dashboard python setup.py bdist_wheel

# 5. Build the hummingbot-api-client wheel (pyproject.toml-based)
WORKDIR /app/hummingbot-api-client
RUN conda run -n dashboard python -m build --wheel

# =================================================================
# STAGE 2: Release Image
# Creates the final, lean image for the Dashboard.
# =================================================================
FROM continuumio/miniconda3:latest AS release

# Install runtime libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends libusb-1.0-0 curl && \
    rm -rf /var/lib/apt/lists/*

# Copy the pre-built conda environment from builder
COPY --from=builder /opt/conda/envs/dashboard /opt/conda/envs/dashboard

WORKDIR /home/dashboard

# 1. Install hummingbot wheel
COPY --from=builder /app/hummingbot-source/dist/hummingbot-*.whl .
RUN /opt/conda/envs/dashboard/bin/pip install --no-deps --no-cache-dir hummingbot-*.whl && rm hummingbot-*.whl

# 2. Install hummingbot-api-client wheel
COPY --from=builder /app/hummingbot-api-client/dist/hummingbot_api_client-*.whl .
RUN /opt/conda/envs/dashboard/bin/pip install --no-deps --no-cache-dir hummingbot_api_client-*.whl && rm hummingbot_api_client-*.whl

# 3. Copy the Dashboard source
COPY hummingbot-dashboard/. .

# Create mount points
RUN mkdir -p /home/dashboard/data

# Expose Streamlit port
EXPOSE 8501

# Entrypoint for Streamlit
ENTRYPOINT ["/opt/conda/envs/dashboard/bin/streamlit", "run", "main.py"]
