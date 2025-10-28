pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh '''
                    # Install Python, pip, curl, docker-compose if not present
                    if ! command -v python3 >/dev/null; then
                        sudo apt-get update
                        sudo apt-get install -y python3 python3-pip curl
                    fi
                    if ! command -v docker-compose >/dev/null; then
                        sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                        sudo chmod +x /usr/local/bin/docker-compose
                    fi
                '''
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest tests/ -v'
            }
        }

        stage('Deploy Stack') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Wait for Flask') {
            steps {
                timeout(time: 90, unit: 'SECONDS') {
                    waitUntil {
                        script {
                            def status = sh(
                                script: 'curl -f http://localhost:5000/ || exit 1',
                                returnStatus: true
                            )
                            return status == 0
                        }
                    }
                }
                echo 'App is running at http://localhost:5000'
            }
        }
    }

    post {
        always { echo 'Pipeline finished.' }
        success { echo 'SUCCESS: All good!' }
        failure { echo 'FAILED: Check logs.' }
    }
}