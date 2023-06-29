FROM 	python:3.11.3-slim
WORKDIR /code
COPY	/manager/requirements /code/requirements
RUN	pip install pip --upgrade
RUN 	pip install --no-cache-dir -U -r /code/requirements
COPY	/manager /code/manager
CMD	["sh", "-c", "uvicorn manager.main:app --host $APP_HOST --port $APP_PORT"]
