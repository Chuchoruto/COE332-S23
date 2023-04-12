
# GENES APP

This project provides data about genes and their IDs
### Data Used

The data used is accessed from the link https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json
It is loaded into the script via API request from the Python requests library as follows

The dataset includes information on all HGNC genes
More info can be found at the link below
https://www.genenames.org/download/archive/

```
import requests
import json

url = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json'
response = requests.get(url)
```


### Script/Flask App
`genes.py`
The Flask App I have created runs the app on a local port and actively queries data from the dataset linked above based on the user's curl input.

| Curl Route  | Method   | Output      |
| ----------- | -------- | ----------- |
| `/data`      | GET |Entire Dataset       |
| `/data`      | POST |Confirmation message of posted data to redis-db |
| `/data`      | DELETE |Confirmation message of deleted data from redis-db |
| `/genes`      | GET |List of all gene HGNC_IDs in the set |
| `/genes/<hgnc_id>`      | GET |Dictionary of the relevant data from the specific HGNC_ID gene|


### INSTRUCTIONS TO RUN

#### MUST DO!!!

Make sure to be in the github repo directory for this project. Then type:
```
mkdir data
```
This ensures that the redis data saves properly

For testing methods 1 and 2, make sure to use a python debug deployment to exec in to and run the curl commands.
Here is an example yaml file for a debug deployment
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: py-debug-deployment
  labels:
    app: py-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: py-app
  template:
    metadata:
      labels:
        app: py-app
    spec:
      containers:
        - name: py39
          image: python:3.9
          command: ['sleep', '999999999']
```

#### Method 1 - Kubernetes Deployment of the App

First git pull this repository

Secondly, kubectl apply -f all of the yaml files except docker-compose.yml
Do the following for all 5 of the flask and redis yml files.
```
kubectl apply -f lucal-flask-deployment.yml
```

This sums up using the prebuilt application.

Use the following to exec into the debug deployment and then begin curl commands
```
kubectl exec -it <python-debug-deployment-name> -- /bin/bash
```

#### Method 2 - Kubernetes Deployment of your own image

Using the provided genes.py and dockerfile, build your own image to your liking.
Use
```
docker build -t <username>/<image-name>:<tag> .
```
In order to run this image in your application, simply change the image name of lucalabardini/genes:hw7.2 to whatever you have just built in the lucal-flask-deployment.yml file
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lucal-test-flask-deployment
  labels:
    username: lucal
    env: test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: lucal-test-flask
  template:
    metadata:
      labels:
        app: lucal-test-flask
        username: lucal
        env: test
    spec:
      containers:
        - name: flask
          image: YOUR_IMAGE_NAME_HERE
          imagePullPolicy: Always
          env:
            - name: lucal-test-redis-service
              value: lucal-test-redis-service
          ports:
            - containerPort: 5000
```
After that, follow the steps for Method 1 and you can begin testing the app

#### Method 3 - pull prebuilt image and run

Pull the docker image from dockerhub using
```
docker pull lucalabardini/genes:1.0
```

Then simply type in the terminal:

```
docker-compose up
```

Then in a separate terminal run curl commands such as
```
curl localhost:5000/data
```


#### Method 4 - Building image from dockerfile

Make sure you are in the directory with the dockerfile and genes.py script


Build your image using the dockerfile
```
docker build -t <username>/genes:<tag> .
```

Push image to docker
```
docker push <username>/genes:<tag>
```

Run the Flask app using the newly built image
Change the image name in yaml file 
```
version: "3"

services:
    redis-db:
        image: redis:7
        ports:
            - 6379:6379
        volumes:
            - ./data:/data
        user: "1000:1000"
    flask-app:
        build:
            context: ./
            dockerfile: ./Dockerfile
        depends_on:
            - redis-db
        image: <username>/genes:<tag>
        ports:
            - 5000:5000
        volumes:
            - ./config.yaml:/config.yaml
```
Then run 
```
docker-compose up
```

Then in a separate terminal run curl commands such as
```
curl 'localhost:5000/data'
```


### Example Input/Output and Usage

#### Important Note
Data must be loaded into the redis database using the data post command before the others work

#### Note
For method 1 be sure to change 'localhost' in the following messages to the IP for the specific flask service
To do so run:
```
kubectl get services
```
This will return something like the following:
```
NAME                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
hello-service              ClusterIP   10.233.20.245   <none>        5000/TCP   8d
lucal-test-flask-service   ClusterIP   10.233.39.205   <none>        5000/TCP   6d5h
lucal-test-redis-service   ClusterIP   10.233.4.216    <none>        6379/TCP   6d5h
```
Pick the CLUSTER-IP in the row that has `<username>-test-flask-service`


Below are examples of certain inputs that the user can put into the separate terminal

Running the command:
```
curl 'localhost:5000/data'
```
Should return the whole dataset which looks something like
```
[
  {
    "_version_": 1761544698598522881,
    "agr": "HGNC:49676",
    "date_approved_reserved": "2014-02-04",
    "date_modified": "2023-01-06",
    "ensembl_gene_id": "ENSG00000269416",
    "entrez_id": "104472717",
    "gene_group": [
      "Long intergenic non-protein coding RNAs"
    ],
    "gene_group_id": [
      1986
    ],
    "hgnc_id": "HGNC:49676",
    "lncipedia": "LINC01224",
    "location": "19p12",
    "location_sortable": "19p12",
    "locus_group": "non-coding RNA",
    "locus_type": "RNA, long non-coding",
    "name": "long intergenic non-protein coding RNA 1224",
    "refseq_accession": [
      "NR_126448"
    ],
    "rna_central_id": [
      "URS00007E4CDE"
    ],
    "status": "Approved",
    "symbol": "LINC01224",
    "uuid": "829eeb97-cff4-43f7-b079-e15adddab334",
    "vega_id": "OTTHUMG00000183272"
  },
  {
    "_version_": 1761544708021026817,
    "agr": "HGNC:8409",
    "alias_symbol": [
      "OST024"
    ],
    "date_approved_reserved": "1999-12-09",
    "date_modified": "2016-10-05",
    "date_name_changed": "2015-12-09",
    "ena": [
      "AA574056"
    ],
    "ensembl_gene_id": "ENSG00000205240",
    "entrez_id": "26637",
    "gene_group": [
      "Olfactory receptors, family 7"
    ],
    "gene_group_id": [
      154
    ],
    "hgnc_id": "HGNC:8409",
    "horde_id": "OR7E36P",
    "location": "13q14.11",
    "location_sortable": "13q14.11",
    "locus_group": "pseudogene",
    "locus_type": "pseudogene",
    "name": "olfactory receptor family 7 subfamily E member 36 pseudogene",
    "prev_name": [
      "olfactory receptor, family 7, subfamily E, member 36 pseudogene"
    ],
    "prev_symbol": [
      "OR7E119P"
    ],
    "pseudogene.org": "PGOHUM00000248383",
    "refseq_accession": [
      "NG_004129"
    ],
    "status": "Approved",
    "symbol": "OR7E36P",
    "uuid": "e1677709-d070-4f81-b52e-5e377cab85a1",
    "vega_id": "OTTHUMG00000016793"
  }
]
```

Running the command:
```
curl -X POST 'localhost:5000/data'
```
Should return a confirmation that the data was posted
```
Data has been posted
```

```
curl -X DELETE 'localhost:5000/data'
```
Should return a confirmation that the data was deleted
```
Data had ben deleted. There are 0 keys in the db
```


```
curl localhost:5000/genes
```
Should return a list of the gene IDs in the set
```
[
  "HGNC:1766",
  "HGNC:16063",
  "HGNC:20024",
  "HGNC:17677",
  "HGNC:51443",
  "HGNC:32025",
  "HGNC:16350",
  "HGNC:15265",
  "HGNC:52950",
  "HGNC:24592",
  "HGNC:15822",
  "HGNC:24352",
  "HGNC:54766",
  "HGNC:26633"
]
```

```
curl localhost:5000/genes/HGNC:1766
```
Should return the information of gene id HGNC:1766
```
{
  "_version_": 1761544682705256448,
  "agr": "HGNC:1766",
  "ccds_id": [
    "CCDS82259",
    "CCDS11993"
  ],
  "date_approved_reserved": "1997-02-10",
  "date_modified": "2023-01-20",
  "date_name_changed": "2016-01-15",
  "ena": [
    "AB035301"
  ],
  "ensembl_gene_id": "ENSG00000081138",
  "entrez_id": "1005",
  "gene_group": [
    "Type II classical cadherins"
  ],
  "gene_group_id": [
    1186
  ],
  "hgnc_id": "HGNC:1766",
  "location": "18q22.1",
  "location_sortable": "18q22.1",
  "locus_group": "protein-coding gene",
  "locus_type": "gene with protein product",
  "mane_select": [
    "ENST00000397968.4",
    "NM_004361.5"
  ],
  "mgd_id": [
    "MGI:2442792"
  ],
  "name": "cadherin 7",
  "omim_id": [
    "605806"
  ],
  "prev_name": [
    "cadherin 7, type 2"
  ],
  "pubmed_id": [
    9615235
  ],
  "refseq_accession": [
    "NM_033646"
  ],
  "rgd_id": [
    "RGD:1306856"
  ],
  "status": "Approved",
  "symbol": "CDH7",
  "ucsc_id": "uc002lkb.4",
  "uniprot_ids": [
    "Q9ULB5"
  ],
  "uuid": "59ea51cf-2caf-4b9e-9624-58c5e6d917ca",
  "vega_id": "OTTHUMG00000132800"
}
```