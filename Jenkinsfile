pipeline {
    agent {
        docker {
            image 'abhirajadhikary06/myflaskapp:latest'
            label 'docker'
            args '''
                -v /var/run/docker.sock:/var/run/docker.sock
                -v /usr/bin/docker:/usr/bin/docker
                --user root
            '''
            reuseNode true
        }
    }

    options {
        timeout(time: 8, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install & Test') {
            parallel {
                stage('Install') {
                    steps {
                        sh 'pip install --upgrade pip --quiet'
                        sh 'pip install -r requirements.txt --quiet'
                    }
                }
                stage('Test') {
                    steps {
                        sh 'pytest tests/ -vv --junitxml=report.xml'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose up -d --remove-orphans'
            }
        }

        stage('Wait for App') {
            steps {
                timeout(time: 60, unit: 'SECONDS') {
                    waitUntil {
                        sh(script: 'curl -f http://localhost:5000/ || exit 1', returnStatus: true) == 0
                    }
                }
                echo 'App is up!'
            }
        }
    }

    post {
        always {
            junit 'report.xml'
            cleanWs()
        }
        success { echo 'Deployed!' }
        failure { echo 'Failed!' }
    }
}