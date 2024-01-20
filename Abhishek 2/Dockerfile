# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including Rust compiler
RUN apt-get update \
    && apt-get install -y libsndfile1 curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y

# Add Rust binaries to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Rust
RUN rustup update

# Copy requirements.txt to the container
COPY ./requirements.txt /app/requirements.txt

#upadted the pip version and installed the librarys in requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

# Copy the rest of your application code
COPY . /app

# Set the entry point
ENTRYPOINT ["python"]

# Set the default command to run your application
CMD ["main.py"]