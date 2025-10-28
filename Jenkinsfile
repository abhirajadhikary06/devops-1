pipeline {
    agent {
        docker {
            image 'abhirajadhikary06/myflaskapp:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock --user root'
            reuseNode true
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest tests/ -v'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Wait for App') {
            steps {
                timeout(time: 90, unit: 'SECONDS') {
                    waitUntil {
                        script {
                            def r = sh(
                                script: 'curl -f http://localhost:5000/ || exit 1',
                                returnStatus: true
                            )
                            return r == 0
                        }
                    }
                }
                echo 'Flask app is UP!'
            }
        }
    }

    post {
        always { echo 'Done.' }
        success { echo 'SUCCESS' }
        failure { echo 'FAILED' }
    }
}