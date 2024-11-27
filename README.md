# Dishcovery


## Installation

For local usage and development, first create an environment (conda or venv).

```
conda create -n dishcovery python=3.10 -y
conda activate dishcovery

pip install -r requirements.txt
```

## Usage

From `Dishcovery` directory, run the following to start the application: 

```
flask --app src.app run --host=0.0.0.0 --port=8000
```