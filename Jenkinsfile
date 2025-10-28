pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
            args '--network host'
        }
    }
    
    environment {
        DOCKER_IMAGE = 'abhirajadhikary06/myflaskapp'
        DOCKER_TAG = 'latest'
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'python -m pytest tests/'
            }
        }
        
        stage('Build and Push Docker Image') {
            agent any  // Switch back to Jenkins agent for Docker operations
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                        sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        sh "docker logout"
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}