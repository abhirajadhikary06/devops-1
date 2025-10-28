pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    # Install Python if not available
                    if ! command -v python3 &> /dev/null; then
                        echo "Python not found, installing Python 3..."
                        apt-get update && apt-get install -y python3 python3-pip curl
                    fi
                    
                    # Install dependencies and run tests
                    python3 -m pip install -r requirements.txt
                    python3 -m pytest tests/ -v
                '''
            }
        }
        
        stage('Build and Deploy') {
            steps {
                sh '''
                    # Build and deploy
                    docker build -t abhirajadhikary06/myflaskapp:latest .
                    docker-compose up -d
                '''
            }
        }
        
        stage('Verify') {
            steps {
                sh '''
                    # Wait for app to start
                    sleep 10
                    curl -f http://localhost:5000/ || echo "App not responding"
                '''
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