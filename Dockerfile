# =================================================================
# STAGE 1: Builder
# Builds a Python 3.12-compatible wheel in a single, consistent environment.
# =================================================================
FROM continuumio/miniconda3:latest AS builder

# Install essential C++ compiler tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Create the final Dashboard environment from its YAML file.
# The path is now relative to the new build context (the parent directory).
COPY hummingbot-dashboard/environment_conda.yml .
RUN conda env create -f environment_conda.yml

# 2. Install the necessary BUILD dependencies for Hummingbot into this environment.
RUN conda run -n dashboard pip install --no-cache-dir cython "numpy<2.0.0" wheel setuptools

# 3. Copy the Hummingbot client source code. This now works because the
# 'hummingbot' folder is inside the build context.
COPY hummingbot ./hummingbot-source

# 4. Build the wheel INSIDE the Python 3.12 Dashboard environment.
WORKDIR /app/hummingbot-source
RUN conda run -n dashboard python setup.py bdist_wheel


# =================================================================
# STAGE 2: Release Image
# Creates the final, lean image for the Dashboard.
# =================================================================
FROM continuumio/miniconda3:latest AS release

# Install only essential runtime libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends libusb-1.0-0 curl && \
    rm -rf /var/lib/apt/lists/*

# Copy the ENTIRE pre-built conda environment from the builder stage.
COPY --from=builder /opt/conda/envs/dashboard /opt/conda/envs/dashboard

# Set the working directory for the Dashboard application
WORKDIR /home/dashboard

# 1. Install the compatible wheel that was just built.
COPY --from=builder /app/hummingbot-source/dist/hummingbot-*.whl .
RUN /opt/conda/envs/dashboard/bin/pip install --no-deps --no-cache-dir hummingbot-*.whl && rm hummingbot-*.whl

# 2. Copy the Dashboard's application source code.
# The path is relative to the new build context.
COPY hummingbot-dashboard/. .

# Create mount points
RUN mkdir -p /home/dashboard/data

# Expose the standard Streamlit port
EXPOSE 8501

# Set the entrypoint to run the application using the absolute path to streamlit.
ENTRYPOINT ["/opt/conda/envs/dashboard/bin/streamlit", "run", "main.py"]