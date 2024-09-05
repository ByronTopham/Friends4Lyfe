pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/ByronTopham/Friends4Lyfe.git'
        DOCKER_IMAGE = 'akanshapal/stock-calculator-final:latest'
        KUBE_NAMESPACE = 'default' // Kubernetes namespace to deploy to
        AWS_CREDENTIALS_ID = 'aws-credentials-id'
        PYTHON_PATH = 'C:\\Users\\pawan\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
        PYTHONHOME = 'C:\\Users\\pawan\\AppData\\Local\\Programs\\Python\\Python312'  // Set PYTHONHOME to the base Python directory
        PYTHONPATH = 'C:\\Users\\pawan\\AppData\\Local\\Programs\\Python\\Python312\\Lib;C:\\Users\\pawan\\AppData\\Local\\Programs\\Python\\Python312\\DLLs'  // Set PYTHONPATH to the library paths
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'git-credentials', url: "${GIT_REPO}"
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run the test cases using the configured Python executable
                    bat "\"${PYTHON_PATH}\" Friends4Lyfe/tests/unit_test.py"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKERHUB_PASS', usernameVariable: 'DOCKERHUB_USER')]) {
                        bat "docker login -u %DOCKERHUB_USER% -p %DOCKERHUB_PASS%"
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
