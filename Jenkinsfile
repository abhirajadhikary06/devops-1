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
        stage('Run Pytest') {
            steps {
                sh 'pytest tests/'
            }
        }
        stage('Run Playwright Tests') {
            steps {
                sh 'playwright install --with-deps'
                sh 'python app.py & sleep 5; pytest e2e/; kill $!'
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker buildx build -t myflaskapp:latest .'
            }
        }
        stage('Deploy with Compose') {
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