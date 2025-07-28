# GPX-Analyzer

# Setup the project

## Clone and install dependencies preferably in a virtual environment

### Clone the repository

```bash

git clone https://github.com/alexgasconn/GPX-Analyzer.git
```

### Install dependencies

```bash
cd GPX-Analyzer
# If you have `uv` installed, you can use it to create the virtual environment and install dependencies
# Otherwise, you can use the standard Python venv module
python3 -m venv .venv # or uv venv
source .venv/bin/activate
pip install -r requirements.txt # or uv pip install -r requirements.txt
```

## Run the project

```bash
streamlit run app.py
```
