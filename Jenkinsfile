pipeline {
    agent any  // Run on Jenkins agent (host), NOT inside python:3.12-slim
    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh 'python3 -m pytest tests/ -vv'
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker buildx build -t myflaskapp:latest .'
            }
        }
        stage('Deploy with Monitoring') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed'
        }
    }
}