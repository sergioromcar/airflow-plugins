export AIRFLOW_HOME="$PWD"
AIRFLOW_VERSION=2.7.0
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
echo $CONSTRAINT_URL
pip install "apache-airflow[mysql,google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
