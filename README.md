# Dishcovery

The app is deployed on dishcovery-app.impaas.uk.


## Instructions for Local Installation / Usage

For local usage and development, first create an environment (conda or venv).

```
conda create -n dishcovery python=3.10 -y
conda activate dishcovery

pip install -r requirements.txt
```

### Usage

From `Dishcovery` directory, run the following to start the application: 

```
flask --app src.app run --host=0.0.0.0 --port=8000
```

## Local PostgreSQL installation

1. Install pip requirements 
2. Install psql locally. On macOS, it is ```brew install postgresql@15``` or ```brew install postgresql```
3. Run the following to check version / enter psql:
```
psql --version # to check psql version
psql postgres 
```
4. If the above does not enter psql, try starting the service ```brew services start postgresql```
5. Create dishcovery user and database using:
```
CREATE ROLE dishcovery WITH LOGIN PASSWORD 'dishcovery';
\du # to check user list
CREATE DATABASE dishcovery_app_db;
python src/database/create_tables.py
```
6. Exit (`\q`)and relogin:
```
psql -U dishcovery -d dishcovery_app_db
\dt # list tables
```
