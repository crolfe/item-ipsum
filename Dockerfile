FROM python:3.9-slim

RUN mkdir -p /app

WORKDIR /app

RUN apt-get update && \
	apt-get install -y \
		build-essential && \
	rm -rf /var/lib/apt/lists/*


ADD requirements.txt .
ADD src ./src

RUN pip3 install -r requirements.txt && rm requirements.txt

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
