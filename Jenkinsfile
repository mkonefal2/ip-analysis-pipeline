pipeline {
    agent any  

    environment {
        GEOIP_DB_PATH = "/var/jenkins_home/GeoLite2-Country.mmdb"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/mkonefal2/ip-analysis-pipeline.git',
                    branch: 'main'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Fetch Blocklist') {
            steps {
                sh 'python scripts/blocklist_collector.py'
            }
        }

        stage('Enrich GeoIP') {
            steps {
                sh 'python scripts/geoip_enrich.py'
            }
        }

        stage('Analyze Data') {
            steps {
                sh 'python scripts/analyze_blocklist.py'
            }
        }

        stage('Archive Report') {
            steps {
                archiveArtifacts artifacts: 'data/blocklist_report.csv', fingerprint: true
            }
        }
    }
}
