FROM ghcr.io/quarto-dev/quarto-full:latest

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    LANG=C.UTF-8 \
    UV_MANAGED_PYTHON=1

# Extra tools for this repo
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    git \
    make \
    gpg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    | gpg --dearmor -o /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Install the TeX packages required by the paper template
RUN tlmgr option repository https://mirror.ctan.org/systems/texlive/tlnet \
    && tlmgr install \
    adjustbox \
    booktabs \
    caption \
    csquotes \
    endfloat \
    footmisc \
    geometry \
    latexmk \
    setspace \
    threeparttable \
    xetex

# uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -sf /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /workspaces

CMD ["/bin/sh"]