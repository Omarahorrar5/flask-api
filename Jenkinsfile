pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        DOCKERHUB_USER = 'omarahorrar'
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

        stage('Trivy scan') {
            steps {
                sh '''
                    docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    -v trivy-cache:/root/.cache/ \
                    aquasec/trivy:latest image \
                    --severity HIGH,CRITICAL \
                    --ignore-unfixed \
                    --exit-code 1 \
                    --no-progress \
                    $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Push image') {
            steps{
                withCredentials([string(credentialsId: 'dockerhub-token', varibale: 'DH_TOKEN')]) {
                    sh '''
                        echo "$DH_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
            post {
                always { sh 'docker logout' }
            }
        }
    }

    post {
        always { cleanWs() }
        success { echo 'pipeline ok' }
        failure { echo 'pipeline failed' }
    }
}