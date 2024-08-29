```python
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import logging
 
app = Flask(__name__)
 
# Set up logging
logging.basicConfig(filename='finance_tracker.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
 
def get_db_connection():
    conn = sqlite3.connect('finance_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn
 
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO transactions (type, amount, category, date)
            VALUES (?, ?, ?, ?)
        ''', (data['type'], data['amount'], data['category'], datetime.now().isoformat()))
        conn.commit()
        logging.info(f"Transaction added: {data}")
        return jsonify({"message": "Transaction added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding transaction: {str(e)}")
        return jsonify({"error": "Failed to add transaction"}), 500
    finally:
        conn.close()
 
@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM transactions')
        transactions = cursor.fetchall()
        logging.info(f"Retrieved {len(transactions)} transactions")
        return jsonify([dict(tx) for tx in transactions])
    except Exception as e:
        logging.error(f"Error retrieving transactions: {str(e)}")
        return jsonify({"error": "Failed to retrieve transactions"}), 500
    finally:
        conn.close()
 
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200
 
if __name__ == '__main__':
    app.run(debug=True)
 
```
 
2. Dockerize the application
 
Our Dockerfile remains the same:
 
```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the current directory contents into the container at /app
COPY . /app
 
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
 
# Make port 5000 available to the world outside this container
EXPOSE 5000
 
# Define environment variable
ENV FLASK_APP=app.py
 
# Run app.py when the container launches
CMD ["flask", "run", "--host", "0.0.0.0"]
 
```
 
Make sure to create a `requirements.txt` file with all the necessary Python packages, which should include Flask and any other dependencies your application needs.
 
3. Set up Kubernetes deployment
 
Let's update our Kubernetes manifests to focus on just deploying our application:
 
 
```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: finance-tracker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: finance-tracker
  template:
    metadata:
      labels:
        app: finance-tracker
    spec:
      containers:
      - name: finance-tracker
        image: your-registry/finance-tracker:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          value: "sqlite:///finance_tracker.db"
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          periodSeconds: 10
          failureThreshold: 3
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          periodSeconds: 60
          failureThreshold: 5
---
apiVersion: v1
kind: Service
metadata:
  name: finance-tracker
spec:
  selector:
    app: finance-tracker
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: finance-tracker
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - finance-tracker.yourdomain.com
    secretName: finance-tracker-tls
  rules:
  - host: finance-tracker.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: finance-tracker
            port: 
              number: 80
 
```
 
4. CI/CD Pipeline
 
Our GitHub Actions workflow remains largely the same, but we'll remove any steps related to Prometheus or Grafana:
 
```yaml
name: CI/CD
 
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
 
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build Docker image
      run: docker build -t your-registry/finance-tracker:${{ github.sha }} .
    - name: Run tests
      run: docker run your-registry/finance-tracker:${{ github.sha }} python -m pytest
    - name: Push to Docker Hub
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push your-registry/finance-tracker:${{ github.sha }}
    - name: Deploy to Kubernetes
      run: |
        echo "${{ secrets.KUBE_CONFIG }}" > kubeconfig
        export KUBECONFIG=kubeconfig
        kubectl set image deployment/finance-tracker finance-tracker=your-registry/finance-tracker:${{ github.sha }}
 
```