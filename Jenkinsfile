pipeline {
    agent any

    environment {
        NAME = "gitops-pipeline"
        VERSION = "${env.BUILD_ID}-${env.GIT_COMMIT}"
        DOCKERHUB_USERNAME = "<replace it with your DockerHub username>"
        GITHUB_TOKEN = credentials("github-token")
        ARGOCD_TOKEN = credentials("argocd-token")
    }

    stages {
        stage('Unit Tests'){
            steps {
               script {
                sh 'pip install -r requirements.txt'
                sh 'python test_app.py'
               }  
            }
        }
        stage('Build Image'){
            steps{
                sh "docker build -t ${NAME} ."
                sh "docker tag ${NAME}:latest ${DOCKERHUB_USERNAME}/${NAME}:${VERSION}"
            }
        } 
        stage('Push Image'){
            steps {
                withDockerRegistry([credentialsId: "dockerhub-id", url: ""]){
                    sh "docker push ${DOCKERHUB_USERNAME}/${NAME}:${VERSION}"
                }
            }
        }
        stage('Clone/Pull repository'){
            steps {
                script {
                    def repoExists = fileExists('ci-cd-infrastructure-code')
                    if (repoExists){
                        dir('ci-cd-infrastructure-code'){
                            sh 'git pull'
                        }
                    }
                    else {
                        sh 'git clone -b feature https://github.com/100daysofdevops/gitops-pipeline-argocd.git'
                    }
                }
            }
        } 
        stage("Updating Kubernetes Manifests"){
            steps{
                dir("ci-cd-infrastructure-code/manifests"){
                    sh "sed -i 's#${DOCKERHUB_USERNAME}/.*#${DOCKERHUB_USERNAME}/${NAME}:${VERSION}#g' deployments.yaml"
                    sh 'cat deployment.yaml'
                }
            }
        }
        stage('Commit & Push'){
            steps {
                dir("ci-cd-infrastructure-code/manifests"){
                    sh "git config user.email 'jenkins@demo.com'"
                    sh "git remote set-url origin https://github.com/100daysofdevops/ci-cd-infrastructure-code.git"
                    sh 'git checkout feature'
                    sh 'git add .'
                    sh "git commit -m 'Updating docker image to version $VERSION'"
                    sh 'git push origin feature' 
                }
            }
        }
        stage('Create PR'){
            steps {
                sh 'bash pullrequest.sh'
            }
        }
    }
}