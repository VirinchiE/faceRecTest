def face_recognition
def dockerHome
def registry = "harbor.cubastion.net"
def targetImage = params.targetImage
def build_num = params.build_number
def harborCred = params.harbor_cred
def argocdServer = params.argocd_server
def argocdAppName = params.argocd_appName
def argocdJenkinsDeployRole = params.argocd_jenkinsDeployRole

pipeline {
    agent any
    options {
        timeout(time: 59, unit: 'MINUTES')
    }
    environment {
    	DOCKER_BUILDKIT='1'
	COMPOSE_DOCKER_CLI_BUILD='1'
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    cleanWs()
                    deleteDir()
                    checkout scm
                }
            }
        }

        stage('Build Image') {
            steps {
                script {
                    face_recog = docker.build("${registry}/${targetImage}:${build_num}")
                }
            }
        }

        stage("Push Image") {
            steps {
                retry(count: 2) {
                    script {
                        docker.withRegistry("https://${registry}", "${harborCred}") {
                            face_recog.push()
                        }
                    }
                }
            }
        }
		
		stage("Refresh k8s container") {
            steps {
                retry(count: 2) {
                    script {
                            withCredentials([string(credentialsId: "${argocdJenkinsDeployRole}", variable: 'ARGOCD_AUTH_TOKEN')]) {
                                sh """
									ARGOCD_SERVER=${argocdServer} argocd app actions run ${argocdAppName} restart --kind StatefulSet
									ARGOCD_SERVER=${argocdServer} argocd --grpc-web app sync ${argocdAppName} --force
									ARGOCD_SERVER=${argocdServer} argocd --grpc-web app wait ${argocdAppName} --timeout 600
                                """
                        }
                    }
                }
            }
        }

        stage("Cleanup") {
            steps {
                script {
                    always {
                        script {
                            try {
                                    sh "docker rmi ${registry}/${targetImage}:${build_num}"
                            } catch (Exception e) {
                                echo "Docker image doesn't exist or already deleted"
                            }
                        }
                        cleanWs()
                        deleteDir()
                    }
                }
            }
        }
    }

    post {
           always {
               script {
                   try {
                        sh "docker rmi ${registry}/${targetImage}:${build_num}"
                  } catch (Exception e) {
                    echo "Docker image doesn't exist or already deleted"
                  }
              }
               cleanWs()
           }
   }
}
