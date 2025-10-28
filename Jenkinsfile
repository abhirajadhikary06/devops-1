pipeline {
    agent {
        docker {
            image 'abhirajadhikary06/myflaskapp:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock --user root'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install & Test') {
            steps {
                sh 'pip install -r requirements.txt'
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
                timeout(time: 1, unit: 'MINUTES') {
                    waitUntil {
                        script {
                            def r = sh(script: 'curl -f http://localhost:5000/ || exit 1', returnStatus: true)
                            return (r == 0)
                        }
                    }
                }
                echo 'App is running!'
            }
        }
    }

    post {
        always {
            echo 'Done!'
        }
    }
}