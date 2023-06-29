FROM 	python:3.11.3-slim
WORKDIR /code
COPY	/monitoring/requirements /code/requirements
RUN	pip install pip --upgrade
RUN 	pip install --no-cache-dir -U -r /code/requirements
COPY	/monitoring /code/monitoring
CMD	["python", "monitoring/main.py"]
