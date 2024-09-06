Connecting kubernetes to prometheus and grafana

### Prerequisites:
- **Amazon EKS Cluster**: Ensure you have an active Amazon EKS cluster.
- **kubectl**: Installed and configured to connect to your EKS cluster.  
- **Helm**: Installed on your local machine.  
  [Reference: Helm Installation](https://helm.sh/docs/intro/install)
---

### Deploying Prometheus on Amazon EKS:

We will use Helm to deploy Prometheus, which simplifies the deployment and management of Kubernetes applications. Follow the steps below:

#### 1. Create a Namespace for Prometheus:
```bash
kubectl create namespace prometheus
```

#### 2. Add the Prometheus Helm Chart Repository:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

#### 3. Deploy Prometheus:
```bash
helm upgrade -i prometheus prometheus-community/prometheus \
    --namespace prometheus \
    --set alertmanager.persistentVolume.storageClass="gp2",server.persistentVolume.storageClass="gp2"
```
This command installs or upgrades the Prometheus deployment in the `prometheus` namespace and configures the persistent volumes using the Amazon EBS `gp2` storage class.

#### 4. Verify the Prometheus Deployment:
```bash
kubectl get pods -n prometheus
```
Some pods may remain in the **Pending** state if the Amazon Elastic Block Store (EBS) CSI driver is not installed.

---

### Setting Up Amazon EBS CSI Driver:

#### 5. Associate an IAM OIDC Provider with Your Cluster:
If not already configured, run the following command:
```bash
eksctl utils associate-iam-oidc-provider --cluster <your-cluster-name> --approve
```

#### 6. Create an IAM Role for the EBS CSI Driver:
```bash
eksctl create iamserviceaccount \
    --name ebs-csi-controller-sa \
    --namespace kube-system \
    --cluster <your-cluster-name> \
    --role-name AmazonEKS_EBS_CSI_DriverRole \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
    --approve
```

#### 7. Manage Amazon EBS CSI Driver as an EKS Add-On:
To simplify management and improve security, you can install the Amazon EBS CSI driver as an Amazon EKS add-on. Run the following command to view available versions:
```bash
aws eks describe-addon-versions --addon-name aws-ebs-csi-driver
```

Add the Amazon EBS CSI add-on using `eksctl`:
```bash
eksctl create addon --name aws-ebs-csi-driver --cluster <your-cluster-name> \
    --service-account-role-arn arn:aws:iam::<account-id>:role/AmazonEKS_EBS_CSI_DriverRole --force
```

Verify the add-on version:
```bash
eksctl get addon --name aws-ebs-csi-driver --cluster <your-cluster-name>
```

Update the add-on if necessary:
```bash
eksctl update addon --name aws-ebs-csi-driver --version <new-version> \
    --cluster <your-cluster-name> --service-account-role-arn arn:aws:iam::<account-id>:role/AmazonEKS_EBS_CSI_DriverRole --force
```

---

### Exposing Prometheus:

#### 8. Verify the Deployment:
Check the status of Prometheus pods:
```bash
kubectl get pods -n prometheus
```
Example output:
```bash
NAME                                             READY   STATUS    RESTARTS   AGE
prometheus-alertmanager-xxx                      1/2     Running   0          48s
prometheus-kube-state-metrics-xxx                1/1     Running   0          48s
prometheus-node-exporter-xxx                     1/1     Running   0          48s
prometheus-server-xxx                            1/2     Running   0          48s
```

#### 9. Label the Prometheus Server Pod:
```bash
kubectl label pod <prometheus-server-pod-name> app=prometheus
```

#### 10. Expose Prometheus using a NodePort Service:
Create a `prometheus-deployment.yml` file with the following content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: prometheus-nodeport
  namespace: prometheus
spec:
  selector:
    app: prometheus
  ports:
    - name: web
      port: 9090
      targetPort: 9090
      protocol: TCP
      nodePort: 30000  # Choose an available port
  type: NodePort
```

Apply the service:
```bash
kubectl apply -f prometheus-deployment.yml
```

#### 11. Access Prometheus:
Use any node's IP with the assigned NodePort (e.g., `http://<node-ip>:30000`) to access Prometheus.

#### 12. Verify Prometheus Targets:
- In the Prometheus UI, navigate to **Status** > **Targets** to view all Kubernetes endpoints connected via service discovery.

---

### Deploying Grafana on Amazon EKS:

#### 1. Add the Grafana Helm Repository:
```bash
helm repo add grafana https://grafana.github.io/helm-charts
```

#### 2. Create a Namespace for Grafana:
```bash
kubectl create namespace grafana
```

#### 3. Create a Grafana YAML Configuration (`grafana.yaml`):
```yaml
datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
    - name: Prometheus
      type: prometheus
      url: http://prometheus-server.prometheus.svc.cluster.local
      access: proxy
      isDefault: true
```

#### 4. Deploy Grafana using Helm:
```bash
helm install grafana grafana/grafana \
    --namespace grafana \
    --set persistence.storageClassName="gp2" \
    --set persistence.enabled=true \
    --set adminPassword='EKS!sAWSome' \
    --values /path/to/grafana.yaml \
    --set service.type=NodePort
```

Replace `adminPassword` with your own password and ensure the path to `grafana.yaml` is correct.

#### 5. Verify Grafana Deployment:
```bash
kubectl get pods -n grafana
```

#### 6. Access Grafana:
Find the NodePort for Grafana:
```bash
kubectl get services -n grafana
```

Access Grafana using the node's IP and NodePort (e.g., `http://<node-ip>:<nodeport>`). Log in with the username `admin` and the password set during deployment.

---

### Conclusion:
You have successfully deployed Prometheus and Grafana on Amazon EKS for monitoring your Kubernetes cluster. These tools provide powerful insights into your infrastructure and applications, enabling efficient troubleshooting and performance monitoring. Explore custom dashboards and set up alerts to meet your specific monitoring needs.

