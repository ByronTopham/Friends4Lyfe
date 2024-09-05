pipeline {
    agent any
    
    environment {
        
        GIT_REPO = 'https://github.com/ByronTopham/Friends4Lyfe.git'
        DOCKER_IMAGE = 'akanshapal/stock-calculator-final:latest'
        KUBE_NAMESPACE = 'default' // Kubernetes namespace to deploy to
        AWS_CREDENTIALS_ID = 'aws-credentials-id'
	PYTHON_PATH = 'C:\\Users\\pawan\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Clone the Git repository
                git branch: 'main', credentialsId: 'git-credentials', url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Run the Docker build command using bat (Windows batch command)
                    bat "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Install Python and required packages
                    bat '%PYTHON_PATH% -m pip install --upgrade pip'
                    bat 'pip install Flask'
                    bat 'pip install pytest'
                    
                    // Run unit tests
                    bat 'pytest tests/unit_test.py'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Replace 'dockerhub-credentials' with your Jenkins Docker credentials ID
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKERHUB_PASS', usernameVariable: 'DOCKERHUB_USER')]) {
                        // Log in to Docker Hub or your Docker registry
                        bat "docker login -u %DOCKERHUB_USER% -p %DOCKERHUB_PASS%"
                        
                        // Push the Docker image
                        bat "docker push ${DOCKER_IMAGE}"
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                withAWS(credentials: "${AWS_CREDENTIALS_ID}", region: 'us-west-2') {
			bat 'kubectl apply -f deployment.yaml'
			bat 'kubectl apply -f network-policy.yaml'
			bat 'kubectl get pods --show-labels'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            cleanWs() // Clean workspace after the pipeline
        }
    }
}
