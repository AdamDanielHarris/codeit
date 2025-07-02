# Docker environment for Python learning with Mamba
FROM mambaorg/micromamba:1.5.6

# Set working directory
WORKDIR /workspace

# Copy environment configuration
COPY environment.yml /tmp/environment.yml

# Create the environment using micromamba
USER root
RUN micromamba create -f /tmp/environment.yml -y && \
    micromamba clean --all --yes

# Initialize micromamba for bash shells
RUN micromamba shell init --shell bash --root-prefix=/opt/conda

# Set up environment activation and create activation script
ENV MAMBA_ROOT_PREFIX=/opt/conda
# Environment variables to fix matplotlib and fontconfig permission issues
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV FONTCONFIG_PATH=/tmp/fontconfig
ENV XDG_CACHE_HOME=/tmp/cache
ENV MPLBACKEND=Agg
RUN echo '#!/bin/bash' > /opt/conda/activate_env.sh && \
    echo 'eval "$(micromamba shell hook --shell bash)"' >> /opt/conda/activate_env.sh && \
    echo 'micromamba activate python-learning' >> /opt/conda/activate_env.sh && \
    echo 'exec "$@"' >> /opt/conda/activate_env.sh && \
    chmod +x /opt/conda/activate_env.sh && \
    mkdir -p /tmp/matplotlib /tmp/fontconfig /tmp/cache && \
    chmod 777 /tmp/matplotlib /tmp/fontconfig /tmp/cache

# Create a non-root user for running the container
RUN useradd -m -s /bin/bash learner && \
    chown -R learner:learner /workspace && \
    echo 'eval "$(micromamba shell hook --shell bash)"' >> /home/learner/.bashrc && \
    echo 'micromamba activate python-learning' >> /home/learner/.bashrc

USER learner

# Set the default command to keep container running with environment activated
CMD ["/opt/conda/activate_env.sh", "tail", "-f", "/dev/null"]
