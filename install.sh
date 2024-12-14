# Run k8s cluster

minikube status
if [[ $? -eq 0 ]]; then   
    echo "Running"; 

    # Installing metrics-server for monitoring CPU utilization.
    kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
    
    # Installing storage provisioner
    kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.30/deploy/local-path-storage.yaml

    # Install ESO Controller for DB secret Management
    helm repo add external-secrets https://charts.external-secrets.io
    helm repo update external-secrets
    helm install external-secrets \
    external-secrets/external-secrets \
        -n external-secrets \
        --create-namespace --wait

    # This is an AWS creds of IAM user with only read access to Secrets Manager.
    kubectl create -f kube-manifests/local-aws-secret.yaml 

    # Connecting to AWS Secrets Manager
    kubectl create -f kube-manifests/secret-store.yaml

    # Retrieving the DB secret from secrets manager & creating a k8s secret.
    kubectl create -f kube-manifests/external-secrets.yaml 

    # Starting the services.
    kubectl apply -f kube-manifests/mysql-pvc.yaml
    kubectl apply -f kube-manifests/mysql.yaml
    kubectl apply -f kube-manifests/webapp.yaml

else   
    echo "Minikube not Running"; 
fi
