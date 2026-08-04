FROM nvidia/cuda:11.8.0-base-ubuntu20.04 as base_build

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

ARG DEBIAN_FRONTEND=noninteractive
ENV CUDNN_VERSION=8.6.0.163
ENV CUDA=11.8

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub && \
    apt-get update && apt-get install -y --no-install-recommends \
        automake \
        build-essential \
        ca-certificates \
        cuda-command-line-tools-11-8 \
        libcublas-11-8 \
        libcublas-dev-11-8 \
        cuda-nvrtc-11-8 \
        cuda-nvrtc-dev-11-8 \
        cuda-nvprune-11-8 \
        cuda-nvcc-11-8 \
        cuda-nvml-dev-11-8 \
        cuda-cudart-dev-11-8 \
        libcufft-dev-11-8 \
        libcurand-dev-11-8 \
        libcusolver-dev-11-8 \
        libcusparse-dev-11-8 \
        curl \
        git \
        libfreetype6-dev \
        libtool \
        libcudnn8=${CUDNN_VERSION}-1+cuda${CUDA} \
        libcudnn8-dev=${CUDNN_VERSION}-1+cuda${CUDA} \
        libcurl3-dev \
        libzmq3-dev \
        mlocate \
        pkg-config \
        python-dev \
        software-properties-common \
        swig \
        unzip \
        wget \
        zip \
        zlib1g-dev \
        python3-distutils \
        python-distutils-extra && \
    find /usr/local/cuda-11.8/lib64/ -type f -name 'lib*_static.a' -not -name 'libcudart_static.a' -delete

# Install python 3.8.
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y \
    python3.8 python3.8-dev python3-pip python3.8-venv && \
    rm -rf /var/lib/apt/lists/* && \
    python3.8 -m pip install pip --upgrade && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 0

# Make python3.8 the default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 0

RUN curl -fSsL -O https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

RUN apt-get install -y gcc
COPY requirements.txt /app/
RUN pip3 install -U pip && pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Keep container running or customize CMD as needed
CMD ["tail", "-f", "/dev/null"]