# RAG-APP

## Requirements

- Python=3.8 or later

### How to Install Python Using Miniconda

1. Download the Miniconda installer for your operating system from the [official Miniconda website](https://docs.conda.io/en/latest/miniconda.html).
2. Run the installer and follow the instructions to complete the installation.
3. Open a terminal (or Anaconda Prompt on Windows).
4. Create a new conda environment with Python 3.8 or later:
    ```sh
    $ conda create --name rag-app python=3.8
    ```
5. Activate the newly created environment:
    ```sh
    $ conda activate rag-app
    ```
6. Verify the installation by checking the Python version:
    ```sh
    $ python --version
    ```
    7. Install the required packages from the `requirements.txt` file:
        ```sh
        $ pip install -r requirements.txt
        ```

You should now have Python 3.8 or later installed in a conda environment.

### (Optional) Setup your command line interface for better readability
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$"
```

### Setup the environment variables
```bash
$ cp .env.example .env
```
Set your enviremonts variables in the `.env` file like `OPENAI_API_KEY` value.

```bash
$ cd docker
$  sudo docker compose up -d
```

### Run the server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```