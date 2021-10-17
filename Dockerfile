FROM python:3.8.5-slim

WORKDIR /pairwise_association
ENV PYTHONPATH=/pairwise_association

COPY ./ /pairwise_association

COPY requirements.txt /pairwise_association/requirements.txt
RUN pip install --user -r requirements.txt

ENTRYPOINT [ "python", "pairwise_association/scripts/main.py" ]