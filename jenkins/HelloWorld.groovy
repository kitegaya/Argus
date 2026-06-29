pipeline {
    agent any
    stages {
        stage('Hello') {
            steps {
                echo 'Hello from Jenkins! 🎉'
                echo 'This pipeline is working correctly.'
            }
        }
    }
}
