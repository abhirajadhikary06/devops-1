pipeline {
    agent { docker { image 'python:3.12-slim' } }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh 'pytest tests/ -vv'
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