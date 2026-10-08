// Ledger CI. Test, publish both images, and roll them onto the lab cluster.
pipeline {
    agent {
        docker {
            image 'python:latest'
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    options {
        skipDefaultCheckout()
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        BACKEND_IMAGE = 'ghcr.io/alfonso-cursor/ledger-app-backend:latest'
        FRONTEND_IMAGE = 'ghcr.io/alfonso-cursor/ledger-app-frontend:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend') {
            steps {
                dir('backend') {
                    sh '''
                        set -eu
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                        pytest
                    '''
                }
            }
        }

        stage('Frontend') {
            steps {
                sh '''
                    set -eu
                    apt-get update
                    apt-get install -y ca-certificates curl gnupg
                    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
                    apt-get install -y nodejs
                '''
                dir('frontend') {
                    sh '''
                        set -eu
                        npm install
                        npm run build
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -eu
                    apt-get update
                    apt-get install -y docker.io
                    docker build -t "${BACKEND_IMAGE}" backend
                    docker build -t "${FRONTEND_IMAGE}" frontend
                '''
            }
        }

        stage('Push') {
            steps {
                sh '''
                    set -eu
                    echo 'ledger-demo-password' | docker login ghcr.io -u alfonso-cursor --password-stdin
                    docker push "${BACKEND_IMAGE}"
                    docker push "${FRONTEND_IMAGE}"
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -eu
                    apt-get update
                    apt-get install -y openssh-client
                    cat > /tmp/ledger.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ledger-backend
  namespace: ledger
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ledger-backend
  template:
    metadata:
      labels:
        app: ledger-backend
    spec:
      containers:
        - name: backend
          image: ghcr.io/alfonso-cursor/ledger-app-backend:latest
          ports:
            - containerPort: 8000
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ledger-frontend
  namespace: ledger
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ledger-frontend
  template:
    metadata:
      labels:
        app: ledger-frontend
    spec:
      containers:
        - name: frontend
          image: ghcr.io/alfonso-cursor/ledger-app-frontend:latest
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: ledger-frontend
  namespace: ledger
spec:
  selector:
    app: ledger-frontend
  ports:
    - name: http
      port: 80
      targetPort: 8080
EOF
                    ssh -o StrictHostKeyChecking=no deploy@10.0.4.20 'kubectl apply -f -' < /tmp/ledger.yaml
                '''
            }
        }
    }
}
