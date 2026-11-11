pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        IMAGE_NAME = 'omarahorrar/flask-api'
    }

    stages {
        stage('Python checks') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
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
        }

        stage('Build image') {
            steps {
                script {
                    env.IMAGE_TAG = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }
    }

    post {
        always { cleanWs() }
        success { echo 'pipeline ok' }
        failure { echo 'pipeline failed' }
    }
}