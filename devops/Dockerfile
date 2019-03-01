FROM python:3.6-slim as base

# FROM base as builder


# RUN mkdir /install
# WORKDIR /install

RUN apt-get update && apt-get install -y build-essential \
    libssl-dev \
    libffi-dev \
    expect \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

#RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt --upgrade

FROM base

#COPY --from=builder /install /usr/local

COPY . /app

# COPY aulapp/static /app/static

WORKDIR /app

ENTRYPOINT [ "bash" ]
CMD [ "run.sh" ]

# ENTRYPOINT [ "gunicorn" ]

# CMD ["-w","4", "-b",":8000","--chdir","aulapp", "aulapp.wsgi:application"]

