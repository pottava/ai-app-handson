FROM python:3.13-slim

# Install related packages
RUN apt-get update && apt-get install -y build-essential vim curl wget jq git gnupg lsb-release
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="/.venv/bin:${PATH}"

# ------------------------------------------------------------------------------
# gcloud
# ------------------------------------------------------------------------------
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
RUN apt-get update && apt-get install -y google-cloud-cli

# ------------------------------------------------------------------------------
# Python Tools
# ------------------------------------------------------------------------------
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# ------------------------------------------------------------------------------
# Node.js Tools
# ------------------------------------------------------------------------------
ENV NPM_VERSION=11.12.1 \
    PNPM_VERSION=10.33.0 \
    RULESYNC_VERSION=7.28.0

RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash - \
    && apt-get install -y nodejs

RUN --mount=type=cache,target=/root/.npm \
    npm install -g "npm@${NPM_VERSION}" --force && \
    npm install -g "pnpm@${PNPM_VERSION}" && \
    npm install -g "rulesync@${RULESYNC_VERSION}" && \
    npm cache clean --force

# ------------------------------------------------------------------------------
# Gemini
# ------------------------------------------------------------------------------
ENV GOOGLE_CLOUD_LOCATION=global \
    GOOGLE_GENAI_USE_VERTEXAI=true \
    GEMINI_CLI_VERSION=0.38.0 \
    ADK_SUPPRESS_GEMINI_LITELLM_WARNINGS=true

RUN npm install -g "@google/gemini-cli@${GEMINI_CLI_VERSION}"

# ------------------------------------------------------------------------------
# Claude Code
# ------------------------------------------------------------------------------
ENV CLAUDE_CODE_USE_BEDROCK=false \
    AWS_REGION=ap-northeast-1 \
    CLAUDE_CODE_USE_VERTEX=false \
    CLOUD_ML_REGION=global \
    ANTHROPIC_MODEL=claude-sonnet-4-6@default \
    ANTHROPIC_SMALL_FAST_MODEL=claude-haiku-4-5@20251001

# ------------------------------------------------------------------------------
# Resolve dependencies for apps
# ------------------------------------------------------------------------------
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync

# Working directory
WORKDIR /workspace
