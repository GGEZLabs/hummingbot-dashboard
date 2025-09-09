# =ger================================================================
# STAGE 1: Builder
# Use mambaforge for a faster, more stable build process.
# =================================================================
FROM condaforge/mambaforge:latest AS builder

# Install essential build tools and clean up in the same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Create the full build environment using Mamba.
# Using 'mamba' instead of 'conda' is much faster and less memory-intensive.
COPY hummingbot-dashboard/environment_conda.yml .
RUN mamba env create -f environment_conda.yml && \
    mamba clean --all --yes

# 2. Install additional build dependencies if needed.
# This line is kept for structural consistency.
RUN mamba run -n dashboard pip install --no-cache-dir cython "numpy<2.0.0" wheel setuptools build

# 3. Copy sources after dependency installation to leverage caching.
COPY hummingbot ./hummingbot-source
COPY hummingbot-api-client ./hummingbot-api-client

# 4. Build the hummingbot wheel.
WORKDIR /app/hummingbot-source
RUN mamba run -n dashboard python setup.py bdist_wheel

# 5. Build the hummingbot-api-client wheel.
WORKDIR /app/hummingbot-api-client
RUN mamba run -n dashboard python -m build --wheel

# =================================================================
# STAGE 2: Release Image
# Creates the final, lean image with a Mamba-built runtime environment.
# =================================================================
FROM condaforge/mambaforge:latest AS release

# Install essential runtime libraries and clean up.
RUN apt-get update && \
    apt-get install -y --no-install-recommends libusb-1.0-0 curl && \
    rm -rf /var/lib/apt/lists/*

# 1. Create the lean runtime environment from the runtime-specific YAML file.
WORKDIR /app
COPY hummingbot-dashboard/runtime-environment.yml .
RUN mamba env create -f runtime-environment.yml && \
    mamba clean --all --yes

WORKDIR /home/dashboard

# 2. Install the pre-built wheels and clean up in a single layer.
COPY --from=builder /app/hummingbot-source/dist/hummingbot-*.whl .
COPY --from=builder /app/hummingbot-api-client/dist/hummingbot_api_client-*.whl .
RUN mamba run -n dashboard pip install --no-deps --no-cache-dir hummingbot-*.whl hummingbot_api_client-*.whl && \
    rm *.whl

# 3. Copy the Dashboard source code.
COPY hummingbot-dashboard/. .

# 4. Aggressive cleanup of the final environment to reduce size.
# This removes tests, docs, pyc files, and static libraries (.a files)
# that are not needed for a runtime image.
RUN find /opt/conda/envs/dashboard -type d -name '__pycache__' -exec rm -r '{}' + && \
    find /opt/conda/envs/dashboard -type f -name '*.pyc' -delete && \
    find /opt/conda/envs/dashboard -type f -name '*.a' -delete && \
    find /opt/conda/envs/dashboard -type d -name 'tests' -exec rm -r '{}' +

# Create mount points.
RUN mkdir -p /home/dashboard/data

# Expose Streamlit port.
EXPOSE 8501

# Set the PATH for cleaner commands.
ENV PATH /opt/conda/envs/dashboard/bin:$PATH

# Entrypoint for Streamlit.
ENTRYPOINT ["streamlit", "run", "main.py"]