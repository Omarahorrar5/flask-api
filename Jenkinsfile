pipeline {
    agent {
        docker { image 'python:3.12-slim' }
    }

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    python -m venv .venv
                    .venv/bin/pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Tests') {
            steps {
                sh '.venv/bin/python -m pytest -v --cov=app --cov-report=xml --junitxml=test-results.xml'
            }
            post {
                always { junit 'test-results.xml' }
            }
        }
    }

    post {
        always { cleanWs() }
        success { echo 'pipeline ok' }
        failure { echo 'pipeline failed' }
    }
}