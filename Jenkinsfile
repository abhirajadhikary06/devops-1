pipeline {
    agent any
    
    environment {
        APP_NAME = 'myflaskapp'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
            }
            steps {
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
                sh 'pip install pytest pytest-flask'
            }
        }
        
        stage('Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
            }
            steps {
                sh 'python -m pytest tests/ -v'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'docker build -t ${DOCKER_USERNAME}/${APP_NAME}:${BUILD_NUMBER} .'
                    sh 'docker tag ${DOCKER_USERNAME}/${APP_NAME}:${BUILD_NUMBER} ${DOCKER_USERNAME}/${APP_NAME}:latest'
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    sh 'docker push ${DOCKER_USERNAME}/${APP_NAME}:${BUILD_NUMBER}'
                    sh 'docker push ${DOCKER_USERNAME}/${APP_NAME}:latest'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'DOCKER_USERNAME=$DOCKER_USERNAME docker-compose down || true'
                    sh 'DOCKER_USERNAME=$DOCKER_USERNAME docker-compose up -d'
                }
            }
        }
    }
    
    post {
        always {
            script {
                sh 'docker logout || true'
                cleanWs()
            }
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}