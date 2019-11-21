FROM continuumio/miniconda

ENV ENV="/root/.bashrc"
WORKDIR /app

RUN apt-get -y install libc++-dev libc++abi-dev

# * Add miniconda's environment and create
ADD environment.yml /environment.yml

RUN conda env create -f /environment.yml

# * Add activate miniconda's command and PATH
RUN echo "source activate lttenv" > ~/.bashrc

ENV PATH /opt/conda/envs/lttenv/bin:$PATH

# * Add supervisor dir and copy configs to dir
RUN mkdir -p /etc/supervisor.d/

COPY etc/supervisor.ini /etc/supervisor.d/

# * Copy application source code to workdir
COPY src .

CMD ["supervisord", "-n"]