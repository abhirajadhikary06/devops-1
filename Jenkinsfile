pipeline {
    // Run every stage inside a Docker container
    agent {
        docker {
            image 'abhirajadhikary06/myflaskapp:latest'   // Your pre-built image
            label 'docker'                                 // Any node with Docker
            args '''
                -v /var/run/docker.sock:/var/run/docker.sock
                -v /usr/bin/docker:/usr/bin/docker
                --user root
            '''
            reuseNode true
        }
    }

    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Tools') {
            steps {
                sh 'python3 --version'
                sh 'pip3 --version'
                sh 'docker --version'
                sh 'docker-compose --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'python3 -m pytest tests/ -vv'
            }
        }

        stage('Docker Build (optional)') {
            when { expression { false } }  // Skip – image already exists
            steps {
                sh 'docker buildx build -t myflaskapp:latest .'
            }
        }

        stage('Deploy with Monitoring') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
            // Optional: clean workspace
            cleanWs()
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}