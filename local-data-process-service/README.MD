## Set up and usage
This service acts as a local data processing middleware between IoT data sources and sinks.

1. **Install dependencies**  
    Run the following command to install the required dependencies:
    ```bash
    pip install -r requirements.txt
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
    python app.py
    ```

    This service operates independently of any web application back-end and processes data between IoT sources and sinks.