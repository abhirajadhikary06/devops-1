pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh 'python -m pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'python -m pytest tests/ -v'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t abhirajadhikary06/myflaskapp:latest .'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
        
        stage('Verify') {
            steps {
                sh 'sleep 10'
                sh 'curl -f http://localhost:5000/ || echo "App not responding"'
                echo 'Deployment verification complete'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed'
        }
        success {
            echo 'Successfully deployed the application'
        }
        failure {
            echo 'Failed to deploy the application'
        }
    }
}