
def dockerRegistry = 'artifactory.enzo.net:8000'

def artifactoryServer = Artifactory.server 'artifactory'
def buildInfo = Artifactory.newBuildInfo()
buildInfo.env.capture = true
buildInfo.retention maxBuilds: 10, deleteBuildArtifacts: true

pipeline {
    agent {
       node {
           label 'xenial'
       }
    }
    
    stages {
        stage('good Luck') {
            steps {
                sh 'echo good LUCK '
            }
        }
      
        stage('Docker -  Build') {
           steps {
               sh 'docker build -t artifactory.enzo.net:8000/analytics:$(date +%Y_%m_%d) .'
               sh 'docker build -t artifactory.enzo.net:8000/r_analytics:$(date +%Y_%m_%d) R_Code/shinyNetwork01/'
               sh 'docker images'
           }
       }

       stage('Docker - Push') {
            environment {
                ARTIFACTORY = credentials('artifactory-jenkins-local')
            }
            steps {
                    sh "docker login ${dockerRegistry} -u ${ARTIFACTORY_USR} -p ${ARTIFACTORY_PSW}"
                    sh 'docker push artifactory.enzo.net:8000/analytics:$(date +%Y_%m_%d)'
                    sh 'docker push artifactory.enzo.net:8000/r_analytics:$(date +%Y_%m_%d)'
                }
     
}}}
