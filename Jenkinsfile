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
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m pip install --user --upgrade pip
                python3 -m pip install --user -r requirements.txt
                python3 -m pip install --user pytest pytest-flask
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest tests/ -v'
            }
        }
        
        stage('Docker Build and Push') {
            agent {
                label 'docker'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                    docker build -t ${DOCKER_USERNAME}/${APP_NAME}:${BUILD_NUMBER} .
                    docker tag ${DOCKER_USERNAME}/${APP_NAME}:${BUILD_NUMBER} ${DOCKER_USERNAME}/${APP_NAME}:latest
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                    docker push ${DOCKER_USERNAME}/${APP_NAME}:${BUILD_NUMBER}
                    docker push ${DOCKER_USERNAME}/${APP_NAME}:latest
                    '''
                }
            }
        }
        
        stage('Deploy Application') {
            agent {
                label 'docker'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                    export DOCKER_USERNAME=$DOCKER_USERNAME
                    docker-compose down || true
                    docker-compose up -d
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                sh 'docker logout || true || echo "Docker logout failed but continuing"'
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