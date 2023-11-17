pipeline {
    agent any
    environment {
        SECRET_FILE = credentials('7f644fde-1fd9-4b1b-ab85-9fd191543eab')
        FIREBASE_FILE = credentials('badf1296-ffc7-4ac9-bc56-7ce989f92c61')// Updatred Firebase_File from jenkins
        SSH_KEY = credentials('cf6dc75c-fb74-4b99-852a-1d83178f6696')
        HOST_IP = credentials('7e089a3f-8c9d-423b-8c55-0c36c0bdc11f')
        HOSTNAME = credentials('a0f18e25-a321-4151-ae71-607e25962dc0')
        GITHUB_TOKEN = credentials('githubtoken')
        PYTHONPATH = "${env.WORKSPACE}/backend"
        
    }
    stages {
            stage('Checkout') {
                steps {
                    checkout scm // Check out your source codes
                }
        }
     stage('Build') {
            steps {
                script {
                withCredentials([file(credentialsId: '7f644fde-1fd9-4b1b-ab85-9fd191543eab', variable: 'SECRET_FILE')]) {
                withCredentials([file(credentialsId: 'cf6dc75c-fb74-4b99-852a-1d83178f6696', variable: 'SSH_KEY')])
                 {
                withCredentials([string(credentialsId: '7e089a3f-8c9d-423b-8c55-0c36c0bdc11f', variable: 'HOST_IP')])
                 { 
                    withCredentials([string(credentialsId: 'a0f18e25-a321-4151-ae71-607e25962dc0', variable: 'HOSTNAME')])
                    
                    {
                 
                    def remote = [:]
                    remote.name = 'EC2 Instance'
                    remote.host = HOST_IP
                    remote.user = HOSTNAME
                    remote.identityFile = SSH_KEY
                    remote.allowAnyHosts = true 
                    sshCommand(remote: remote, command: """
                        sudo docker --version
                        cd FerrisWheel_3/FerrisWheel
                        git reset --hard HEAD
                        git pull https://$GITHUB_TOKEN@github.com/tzw99556/FerrisWheel.git
                        cd docker
                        sh start.sh
                        echo "Sucess"
                    """, sudo: true)
                 
                    }
                    
                 }
                }
                }
            }
            }
        }
        
        // stage('Build') {
        //     steps {
        //          script {
        //             def currentWorkspace = env.WORKSPACE
        //             echo "Current workspace: $currentWorkspace"
        //             withCredentials([file(credentialsId: '7f644fde-1fd9-4b1b-ab85-9fd191543eab', variable: 'SECRET_FILE')]) {
        //             sh "echo 'The secret file path is: $SECRET_FILE'"
        //                  // Navigate to the Python back-end directory
        //             withCredentials([file(credentialsId: 'badf1296-ffc7-4ac9-bc56-7ce989f92c61', variable: 'FIREBASE_FILE')]) 
        //             {
                        
        //              sh "echo 'My secret text is: $FIREBASE_FILE'"

        //             }
        //             }
        //          }
        //     }
        // }
        stage('OWASP Dependency-Check Vulnerabilities') {
        steps {
        dependencyCheck additionalArguments: ''' 
                    -o './'
                    -s './'
                    -f 'ALL' 
                    --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
        
            dependencyCheckPublisher pattern: 'dependency-check-report.xml'
      }
    }
        stage('Test') {
            steps {
                 script {
                    withCredentials([file(credentialsId: '7f644fde-1fd9-4b1b-ab85-9fd191543eab', variable: 'SECRET_FILE')]) {
                    withCredentials([file(credentialsId: 'badf1296-ffc7-4ac9-bc56-7ce989f92c61', variable: 'FIREBASE_FILE')]) 
                    {
                    def currentWorkspace = env.WORKSPACE
                    def backendDirectory = "$currentWorkspace/backend"
                    def curlDirectory = "$currentWorkspace/backend/app/tests"
                    echo "Current workspace: $currentWorkspace"
                    // Go to the curlDirectory and run commands
                    dir(curlDirectory) {
                        sh"python curl.py"
                    }
                    sh "pip install pytest"
                    sh "pip install Pillow"
                    dir(backendDirectory) {
                    sh "pytest"
                }
                }
                      }
                   
                 }
            }
        }
    }
    post {
        success {
            script {
                // Actions to perform on successful builds
                echo 'Build successful'
                cleanWs()
            }
        }
        failure {
            script {
                echo 'Build failed'
                // Actions to perform on build failures
                cleanWs()
            }
        }
    }
}