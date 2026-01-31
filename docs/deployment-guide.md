# SmartContent AI - Production Deployment Guide

## 🚀 Deployment Overview

This guide covers deploying SmartContent AI to production using Kubernetes on AWS EKS with best practices for scalability, security, and monitoring.

## 📋 Prerequisites

### Required Tools
- AWS CLI v2.x
- kubectl v1.28+
- Helm v3.x
- Docker v20.x+
- Terraform v1.6+

### AWS Resources
- EKS Cluster (v1.28+)
- RDS PostgreSQL (v15+)
- ElastiCache Redis (v7+)
- S3 Buckets for storage
- CloudFront CDN
- Application Load Balancer
- Route53 for DNS

## 🏗️ Infrastructure Setup

### 1. Terraform Infrastructure

```bash
# Clone and setup infrastructure
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var-file="production.tfvars"

# Apply infrastructure
terraform apply -var-file="production.tfvars"
```

### 2. EKS Cluster Configuration

```yaml
# infrastructure/kubernetes/cluster-config.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: smartcontent-ai-prod
  region: us-east-1
  version: "1.28"

nodeGroups:
  - name: api-nodes
    instanceType: t3.large
    minSize: 2
    maxSize: 10
    desiredCapacity: 3
    volumeSize: 50
    ssh:
      allow: false
    iam:
      withAddonPolicies:
        autoScaler: true
        cloudWatch: true
        ebs: true
    labels:
      workload: api
    taints:
      - key: workload
        value: api
        effect: NoSchedule

  - name: ml-nodes
    instanceType: g4dn.xlarge
    minSize: 1
    maxSize: 5
    desiredCapacity: 2
    volumeSize: 100
    ssh:
      allow: false
    labels:
      workload: ml
    taints:
      - key: workload
        value: ml
        effect: NoSchedule

addons:
  - name: vpc-cni
  - name: coredns
  - name: kube-proxy
  - name: aws-ebs-csi-driver
```

## 🐳 Container Images

### Build and Push Images

```bash
# Build backend image
docker build -t smartcontent-ai/backend:v1.0.0 ./backend
docker tag smartcontent-ai/backend:v1.0.0 $ECR_REGISTRY/smartcontent-ai/backend:v1.0.0
docker push $ECR_REGISTRY/smartcontent-ai/backend:v1.0.0

# Build frontend image
docker build -t smartcontent-ai/frontend:v1.0.0 ./frontend
docker tag smartcontent-ai/frontend:v1.0.0 $ECR_REGISTRY/smartcontent-ai/frontend:v1.0.0
docker push $ECR_REGISTRY/smartcontent-ai/frontend:v1.0.0

# Build ML pipeline image
docker build -t smartcontent-ai/ml-pipeline:v1.0.0 ./ml-pipelines
docker tag smartcontent-ai/ml-pipeline:v1.0.0 $ECR_REGISTRY/smartcontent-ai/ml-pipeline:v1.0.0
docker push $ECR_REGISTRY/smartcontent-ai/ml-pipeline:v1.0.0
```

## ☸️ Kubernetes Deployment

### 1. Namespace and RBAC

```yaml
# infrastructure/kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: smartcontent-ai
  labels:
    name: smartcontent-ai
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: smartcontent-ai-sa
  namespace: smartcontent-ai
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT:role/SmartContentAI-ServiceRole
```

### 2. ConfigMaps and Secrets

```yaml
# infrastructure/kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: smartcontent-ai-config
  namespace: smartcontent-ai
data:
  ENVIRONMENT: "production"
  API_V1_PREFIX: "/api/v1"
  RATE_LIMIT_REQUESTS: "1000"
  RATE_LIMIT_WINDOW: "3600"
  PROMETHEUS_ENABLED: "true"
---
apiVersion: v1
kind: Secret
metadata:
  name: smartcontent-ai-secrets
  namespace: smartcontent-ai
type: Opaque
data:
  SECRET_KEY: <base64-encoded-secret>
  DATABASE_URL: <base64-encoded-db-url>
  OPENAI_API_KEY: <base64-encoded-openai-key>
  PINECONE_API_KEY: <base64-encoded-pinecone-key>
```

### 3. Backend Deployment

```yaml
# infrastructure/kubernetes/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartcontent-ai-backend
  namespace: smartcontent-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smartcontent-ai-backend
  template:
    metadata:
      labels:
        app: smartcontent-ai-backend
    spec:
      serviceAccountName: smartcontent-ai-sa
      nodeSelector:
        workload: api
      tolerations:
        - key: workload
          value: api
          effect: NoSchedule
      containers:
      - name: backend
        image: $ECR_REGISTRY/smartcontent-ai/backend:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          valueFrom:
            configMapKeyRef:
              name: smartcontent-ai-config
              key: ENVIRONMENT
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: smartcontent-ai-secrets
              key: DATABASE_URL
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: smartcontent-ai-secrets
              key: OPENAI_API_KEY
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: smartcontent-ai-backend-service
  namespace: smartcontent-ai
spec:
  selector:
    app: smartcontent-ai-backend
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### 4. Frontend Deployment

```yaml
# infrastructure/kubernetes/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartcontent-ai-frontend
  namespace: smartcontent-ai
spec:
  replicas: 2
  selector:
    matchLabels:
      app: smartcontent-ai-frontend
  template:
    metadata:
      labels:
        app: smartcontent-ai-frontend
    spec:
      nodeSelector:
        workload: api
      tolerations:
        - key: workload
          value: api
          effect: NoSchedule
      containers:
      - name: frontend
        image: $ECR_REGISTRY/smartcontent-ai/frontend:v1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "https://api.smartcontent.ai"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: smartcontent-ai-frontend-service
  namespace: smartcontent-ai
spec:
  selector:
    app: smartcontent-ai-frontend
  ports:
  - port: 80
    targetPort: 3000
  type: ClusterIP
```

### 5. ML Pipeline Deployment

```yaml
# infrastructure/kubernetes/ml-pipeline-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartcontent-ai-ml-pipeline
  namespace: smartcontent-ai
spec:
  replicas: 2
  selector:
    matchLabels:
      app: smartcontent-ai-ml-pipeline
  template:
    metadata:
      labels:
        app: smartcontent-ai-ml-pipeline
    spec:
      nodeSelector:
        workload: ml
      tolerations:
        - key: workload
          value: ml
          effect: NoSchedule
      containers:
      - name: ml-pipeline
        image: $ECR_REGISTRY/smartcontent-ai/ml-pipeline:v1.0.0
        ports:
        - containerPort: 8001
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: smartcontent-ai-secrets
              key: OPENAI_API_KEY
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
            nvidia.com/gpu: 1
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
        volumeMounts:
        - name: model-storage
          mountPath: /app/models
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: ml-models-pvc
```

## 🔧 Ingress and Load Balancing

### AWS Load Balancer Controller

```yaml
# infrastructure/kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: smartcontent-ai-ingress
  namespace: smartcontent-ai
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:ACCOUNT:certificate/CERT-ID
    alb.ingress.kubernetes.io/ssl-redirect: '443'
    alb.ingress.kubernetes.io/healthcheck-path: /health
spec:
  rules:
  - host: app.smartcontent.ai
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: smartcontent-ai-frontend-service
            port:
              number: 80
  - host: api.smartcontent.ai
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: smartcontent-ai-backend-service
            port:
              number: 80
```

## 📊 Monitoring and Observability

### Prometheus and Grafana

```bash
# Install Prometheus using Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --values infrastructure/helm/prometheus-values.yaml

# Install Grafana dashboards
kubectl apply -f infrastructure/kubernetes/grafana-dashboards.yaml
```

### Logging with ELK Stack

```yaml
# infrastructure/kubernetes/elasticsearch.yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: smartcontent-ai-es
  namespace: logging
spec:
  version: 8.11.0
  nodeSets:
  - name: default
    count: 3
    config:
      node.store.allow_mmap: false
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          resources:
            requests:
              memory: 2Gi
              cpu: 1
            limits:
              memory: 4Gi
              cpu: 2
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
        storageClassName: gp3
```

## 🔒 Security Configuration

### Network Policies

```yaml
# infrastructure/kubernetes/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: smartcontent-ai-network-policy
  namespace: smartcontent-ai
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
    - protocol: TCP
      port: 3000
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 5432
    - protocol: TCP
      port: 6379
```

### Pod Security Standards

```yaml
# infrastructure/kubernetes/pod-security-policy.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: smartcontent-ai
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy-production.yml
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Login to Amazon ECR
      uses: aws-actions/amazon-ecr-login@v2
    
    - name: Build and push images
      run: |
        docker build -t $ECR_REGISTRY/smartcontent-ai/backend:$GITHUB_SHA ./backend
        docker push $ECR_REGISTRY/smartcontent-ai/backend:$GITHUB_SHA
        
        docker build -t $ECR_REGISTRY/smartcontent-ai/frontend:$GITHUB_SHA ./frontend
        docker push $ECR_REGISTRY/smartcontent-ai/frontend:$GITHUB_SHA
    
    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --name smartcontent-ai-prod
        kubectl set image deployment/smartcontent-ai-backend smartcontent-ai-backend=$ECR_REGISTRY/smartcontent-ai/backend:$GITHUB_SHA -n smartcontent-ai
        kubectl set image deployment/smartcontent-ai-frontend smartcontent-ai-frontend=$ECR_REGISTRY/smartcontent-ai/frontend:$GITHUB_SHA -n smartcontent-ai
        kubectl rollout status deployment/smartcontent-ai-backend -n smartcontent-ai
        kubectl rollout status deployment/smartcontent-ai-frontend -n smartcontent-ai
```

## 📈 Auto-Scaling Configuration

### Horizontal Pod Autoscaler

```yaml
# infrastructure/kubernetes/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: smartcontent-ai-backend-hpa
  namespace: smartcontent-ai
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: smartcontent-ai-backend
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Cluster Autoscaler

```yaml
# infrastructure/kubernetes/cluster-autoscaler.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.28.0
        name: cluster-autoscaler
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/smartcontent-ai-prod
```

## 🔄 Backup and Disaster Recovery

### Database Backups

```bash
# Automated RDS snapshots
aws rds create-db-snapshot \
  --db-instance-identifier smartcontent-ai-prod \
  --db-snapshot-identifier smartcontent-ai-backup-$(date +%Y%m%d-%H%M%S)

# Cross-region backup replication
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier smartcontent-ai-backup-latest \
  --target-db-snapshot-identifier smartcontent-ai-backup-dr \
  --source-region us-east-1 \
  --target-region us-west-2
```

### Application Data Backup

```yaml
# infrastructure/kubernetes/backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: smartcontent-ai-backup
  namespace: smartcontent-ai
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15-alpine
            command:
            - /bin/bash
            - -c
            - |
              pg_dump $DATABASE_URL | gzip | aws s3 cp - s3://smartcontent-ai-backups/db-backup-$(date +%Y%m%d-%H%M%S).sql.gz
          restartPolicy: OnFailure
```

## 🚨 Alerting and Incident Response

### Prometheus Alerting Rules

```yaml
# infrastructure/kubernetes/alert-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: smartcontent-ai-alerts
  namespace: monitoring
spec:
  groups:
  - name: smartcontent-ai
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High error rate detected"
        description: "Error rate is {{ $value }} errors per second"
    
    - alert: HighMemoryUsage
      expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "High memory usage"
        description: "Memory usage is above 90%"
```

## 📝 Post-Deployment Checklist

### Verification Steps

1. **Health Checks**
   ```bash
   kubectl get pods -n smartcontent-ai
   kubectl get services -n smartcontent-ai
   kubectl get ingress -n smartcontent-ai
   ```

2. **Application Testing**
   ```bash
   curl -f https://api.smartcontent.ai/health
   curl -f https://app.smartcontent.ai
   ```

3. **Monitoring Verification**
   - Check Grafana dashboards
   - Verify Prometheus targets
   - Test alerting rules

4. **Security Validation**
   - SSL certificate verification
   - Network policy testing
   - Access control validation

### Performance Optimization

1. **Database Optimization**
   - Connection pooling configuration
   - Query performance monitoring
   - Index optimization

2. **Caching Strategy**
   - Redis cache hit rates
   - CDN performance metrics
   - Application-level caching

3. **Resource Optimization**
   - CPU and memory utilization
   - Auto-scaling effectiveness
   - Cost optimization analysis

This deployment guide ensures a production-ready, scalable, and secure deployment of SmartContent AI with comprehensive monitoring, backup, and disaster recovery capabilities.