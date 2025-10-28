pipeline {
    agent {
        docker {
            image 'abhirajadhikary06/myflaskapp:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock --user root'
            reuseNode true
        }
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Python Packages') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest tests/ -v'
            }
        }

        stage('Deploy App') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Wait for Flask') {
            steps {
                timeout(time: 90, unit: 'SECONDS') {
                    waitUntil {
                        def result = sh(
                            script: 'curl -f http://localhost:5000/ || exit 1',
                            returnStatus: true
                        )
                        return result == 0
                    }
                }
                echo 'Flask app is UP!'
            }
        }
    }

    post {
        always {
            echo 'Build finished.'
        }
        success {
            echo 'SUCCESS: App is running!'
        }
        failure {
            echo 'FAILED: Check logs.'
        }
    }
}