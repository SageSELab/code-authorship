# syntax=docker/dockerfile:1
#
# Replication environment for "Reassessing Code Authorship Attribution in the
# Era of Language Models" (TOSEM 2026).
#
# Two targets share one build:
#
#   gpu  - CUDA 12.1 + cuDNN 8. Needed for fine-tuning, the explainers and the
#          adversarial attacks. CUDA 12.1 is not arbitrary: the pinned
#          torch==2.1.2 and nvidia-*-cu12==12.1.* wheels in requirements.txt
#          were built against it. Requires an x86_64 host — those wheels have
#          no arm64 build.
#   cpu  - No CUDA. Enough for path-context generation, the RQ1/RQ2/RQ3
#          analysis and plotting scripts, the R figures, and the
#          adversarial-rule unit tests. This is what the smoke test runs.
#
# Build both:
#   docker compose build caa-gpu caa-cpu
#
# Build one directly:
#   docker build -f docker/Dockerfile --target cpu -t caa:cpu .

# ---------------------------------------------------------------------------
# Base layer: OS packages, Python, R, and the Tree-sitter grammars.
# ---------------------------------------------------------------------------
ARG BASE_IMAGE=ubuntu:22.04
FROM ${BASE_IMAGE} AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# build-essential provides the gcc/g++ used to compile the Tree-sitter
# grammars. fonts-liberation matters more than it looks: u-test.py and
# necessity_sufficiency.py request "Times New Roman"/"Liberation Serif", and
# without it matplotlib silently substitutes a different font, changing figure
# metrics. nodejs/npm are only a fallback for grammars that ship without a
# pre-generated parser.c.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        fonts-liberation \
        git \
        libgomp1 \
        nodejs \
        npm \
        python3.10 \
        python3.10-dev \
        python3-pip \
        r-base \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && python -m pip install --upgrade "pip==24.0" "setuptools==69.5.1" "wheel==0.43.0"

# R packages for the orthogonality Venn diagrams (venn-diagram.r,
# orthogonality.r). Pinned to a Posit Package Manager snapshot so the image is
# reproducible rather than tracking CRAN HEAD.
RUN Rscript -e "install.packages( \
        c('venn', 'sets', 'jsonlite'), \
        repos = 'https://packagemanager.posit.co/cran/__linux__/jammy/2024-12-02', \
        Ncpus = parallel::detectCores())" \
    && Rscript -e "library(venn); library(sets); library(jsonlite)"

# Compile the Tree-sitter grammars once, into a location outside the bind mount
# so a `docker compose run` never has to rebuild them.
ENV TREE_SITTER_SO_DIR=/opt/tree-sitter-so
COPY scripts/build-tree-sitter.sh /opt/bin/build-tree-sitter.sh
RUN chmod +x /opt/bin/build-tree-sitter.sh \
    && TREE_SITTER_SRC_DIR=/tmp/tree-sitter-src /opt/bin/build-tree-sitter.sh "${TREE_SITTER_SO_DIR}" \
    && rm -rf /tmp/tree-sitter-src

# Hugging Face cache lives on a named volume (see docker-compose.yml) so
# CodeLlama-7B is not re-downloaded on every run.
ENV HF_HOME=/opt/hf-cache
RUN mkdir -p "${HF_HOME}"

WORKDIR /workspace

# ---------------------------------------------------------------------------
# Python dependencies. Split per target because the torch wheels differ.
# ---------------------------------------------------------------------------
FROM base AS deps-gpu
# The pinned nvidia-*-cu12 wheels are published for x86_64 only, so this target
# cannot build on an arm64 host (e.g. an Apple Silicon Mac). Fail here with an
# actionable message rather than several minutes later with an opaque pip
# resolution error.
RUN arch="$(uname -m)"; \
    if [ "$arch" != "x86_64" ]; then \
        echo "ERROR: the GPU image requires an x86_64 host; this is ${arch}." >&2; \
        echo "The pinned CUDA 12.1 wheels (nvidia-*-cu12) have no ${arch} build." >&2; \
        echo "On Apple Silicon or other arm64 machines, use the CPU target instead:" >&2; \
        echo "    docker compose build caa-cpu" >&2; \
        exit 1; \
    fi
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt

FROM base AS deps-cpu
COPY requirements-cpu.txt /tmp/requirements-cpu.txt
RUN python -m pip install -r /tmp/requirements-cpu.txt

# ---------------------------------------------------------------------------
# Final images. A non-root user matching the host UID/GID keeps everything the
# scripts write into the bind-mounted repository (models/, results/,
# explanations/, *.pdf) owned by the host user instead of root.
# ---------------------------------------------------------------------------
FROM deps-gpu AS gpu
ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" -o caa \
    && useradd -m -u "${UID}" -g "${GID}" -o -s /bin/bash caa \
    && chown -R "${UID}:${GID}" /opt/hf-cache
USER caa
CMD ["bash"]

FROM deps-cpu AS cpu
ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" -o caa \
    && useradd -m -u "${UID}" -g "${GID}" -o -s /bin/bash caa \
    && chown -R "${UID}:${GID}" /opt/hf-cache
USER caa
ENV CUDA_VISIBLE_DEVICES=""
CMD ["bash"]
