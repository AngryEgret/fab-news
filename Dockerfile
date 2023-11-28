FROM python:3.11-slim

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}

COPY . /src
WORKDIR /src

RUN useradd -m -r user && \
    chown user /src
USER user
ENV PATH /home/user/.local/bin:$PATH

RUN pip install .

ENTRYPOINT ["/tini", "--"]

CMD ["fab-news", "--help"]
