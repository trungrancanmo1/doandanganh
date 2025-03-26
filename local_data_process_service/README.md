## Set up and usage
This service acts as a local data processing middleware between IoT data sources and sinks.

1. **Install dependencies**  
    Run the following command to install the required dependencies using Poetry:
    ```bash
    poetry install
    ```

    Alternatively, if you are in a development environment, use:
    ```bash
    poetry install --with dev
    ```

2. **Configure environment variables**  
    Set up the environment variables either by exporting them manually or using a `.env` file.

    To export manually:
    ```bash
    export EMQX_USER_NAME=<Your EMQX username>
    export EMQX_PASSWORD=<Your EMQX password>
    export EMQX_URL=<Your EMQX broker URL>
    ```

    Alternatively, create a `.env` file in the root directory and add:
    ```
    EMQX_USER_NAME=
    EMQX_PASSWORD=
    EMQX_URL=
    ```

3. **Run the service**  
    Start the local data processing service to handle IoT data streams by running:

    ```bash
    docker start <your-redis-server> # to start the message queue used by celery

    poetry run python -m local_data_process_service.app # to run the mqtt_client

    poetry run celery -A local_data_process_service.capp worker --loglevel=info # to run the celery workers

    ```

    This service operates independently of any web application back-end and processes data between IoT sources and sinks.