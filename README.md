## User Management Flask Application

This is a simple python flask application that allows to read & add users details in a mysql database.

### Features

Add User: Submit a form with the user's name and email. The application ensures that the email is unique and inserts the user into the database.

View Users: Displays a list of all users stored in the database, including their ID, name, and email.

Health Check: Provides a simple health check endpoint (/healthz) that returns a success message if the application can connect to the database.
Key Components


### How it works?

When the application starts, init_db() function ensures database exists & user table is created.

/ - Displays user management home page.

/add_user - Endpoint for adding a new user to the database.

/users - To Read the existing user records

/healthz - Endpoint to check the status of DB connection.


### How to start?


#### Prerequisites

Ensure Minikube installed and running.

Update the values in kube-manifests/local-aws-secret.yaml

This application will be deployed on a Minikube Kubernetes cluster, which provides an isolated and manageable environment for testing and development purposes. Ensure that Minikube is running and configured properly before deploying the application.

Execute the following command to install dependencies and start the application:

```sh
sh ./install.sh
```

### Port-forwarding 

kubectl port-forward svc/webapp-service 80:80 

Visit your browser at http://localhost:80/

### Cleaning up cluster

```sh
kubectl delete -f kube-manifests/
minikube delete
```


