FROM python:3.9
WORKDIR /app
RUN apt-get update \
    && apt-get install -y libsndfile1 curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup update
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["main.py"]
