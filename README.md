# Learning-Pro-Django
Learning Pro Django skills and techniques and trying out

## PostgreSQL Setup & Utilities

For handling multiple versions of PostgreSQL in your system,

`sudo service postgresql status`
`sudo service postgresql start <version>`

For e.g. to start just the PostgreSQL version 16 use,

`sudo service postgresql start 16`

If you are running on Linux machine with `supervisor` enabled then most probably at the port 8000 *Apache2* would be running,
and this would interfere with the default port at which the *django* test web server runs hence to find out which service is running at which port,

`sudo lsof -t -i tcp:8000`

Here,

1. sudo means `su` `do` stating switch user or substitute user which can be used to do / perform some action
2. lsof means list open files, which can be used to list the files which are consuming a certain protocol as well
3. `-t` states listing only the concise PIDs of all the files that are listed
4. `-i` is used to select by IPv[46] address
5. `tcp:8080` is the specific IPv4 or IPv6 address using port 8000 which we want to know about

## Docker

[REFERENCE](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/#Why-should-you-containerize-Postgres)

For starting fresh and deleting all the current or previous Docker containers and volumes use,

`docker system prune --all`

`docker volume prune`

### Containerization

For taking a simple example of PostgreSQL database hosted using Containerization using Docker, why should we actually do it?

There are few points which lists out the advantages of containerizing your Database,

1. Containerizing separates your data from the database application.
  Meaning that if in case there is any damage or unexpected failure in the database then the data won't be harmed at all
  and another container can be launced.

2. Using containerization, we can spin and deploy PostgreSQL anywhere we need it.

3. Rapid development through pre-defined config which is very easy to spin and deploy whereas local installation and performing additional configuration etc takes deeper knowledge and time.

PostgreSQL Docker Official Image(DOI) is the official image which tells the PostgreSQL how to behave and interact with data while the container runs on this image.

**Production** or not? -> While it's totally possible to use this PostgreSQL Docker containers in Production but scaling and maintaing many containers can be challenging so it's best suited use case is in development.

### Postgres in Docker

Easily pull the Postgres image from Docker Hub using the `pull` command,

`docker pull postgres`

Starting a postgres container using a basic command will look like,

`docker run --name postgres-container -e POSTGRES_PASSWORD=somepass -d postgres`

To connect with this docker container with bash use,

`docker exec -it postgres-container bash`

Above command creates a docker container named

1. postgres-container(`--name` denotes the container name)
2. `-e` denotes the environment variables to pass to the container
3. -d means in detached state and just print the container ID
4. postgres is the non keyword argument which is the IMAGE name to use while deploying this container

A *docker-compose.yml* file will contain services in it, for e.g.

```
services:
  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_PASSWORD: dockerpostgrespass
    volumes:
      - pgdata: /var/lib/postgresql/data

volumes:
  pgdata:
    driver: local
```

There are few other options which can be used in place of restart parameter, like *unless-stopped* which will keep on restarting the docker container unless we stop it explicitly.

One thing missing in the above service config is the port connection, how do we actually connect to this Postgres DB outside the container, for that we have to mention which port to open to in the container with outside.

```
services:
  db:
    image: postgres
    restart: unless-stopped
    port:
      - "5432:5432"
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: learning_user
      POSTGRES_PASSWORD: dockerpostgrespass
    volumes:
      - pgdata: /var/lib/postgresql/data

volumes:
  pgdata:
    driver: local
```

Notice how in the last service configuration of our PostgreSQL databased we didn't mention the environment variables like
`POSTGRES_DB`, `POSTGRES_USER`. These env vars are actually the name of the database and the username(owner of the db) using 
which we will connect to this docker db. One thing we might miss here is the volume, so our volume is not harmed or affected everytime we do `docker-compose -f docker-compose.yml up -d` to start the docker container or `docker-compose -f docker-compose.yml down` to bring our container down and so the data has been created with the previous configuration and does not actually has our new username and database created in it, for this either we can delete the existing volume using `docker volume rm <volume-name>`(you can find the volume name using `docker volume ls`) or you can attach a new volume to this container by editing the volume name and restarting the docker container.

docker-compose file comprises of services, in our case we have used volume as well so as to separate our container from the 
data and then defining the volume in the service to be used as the data storage location.

# Deployment

We will walk through some of the best ways, a Django app can be deployed.

## Gunicorn, Nginx, HTTPS

[REFERENCE](https://realpython.com/django-nginx-gunicorn/)

AWS -> Learned how to create User using two methods,

1. Identity Center User
  - Requires linking to an existing group or AWS Account which should define the permission sets for this Identity User.

2. IAM User
  - Permission policies can be directly attached to this user and given access.

#### EC2 Key Pair

Before going on to create the EC2 instance, you have to create a Key Pair first, this Key Pair will belong to this region
only and for each region a new Key Pair needs to be created in order to SSH into that region's instances.

Open EC2 Console -> Navigation Pane -> Network & Security -> Key Pairs -> Create Key Pair

After you create a key pair, it will automatically get stored in your system through the browser. You must also ensure that only you have access to read this key pair in your system so use the change mode command(chmod) to give proper permissions,
for .e.g

`chmod 400 <key-pair-file-name.pem/ppk>`

.pem -> is for connecting with the OpenSSH client
.ppk -> is for connecting using the Putty SSH remote login tool

`400` here is the octal value for the permission which means that 4(read - r) permission has been given only to the current user/owner of this file and `00` to the group members(members excluding the current user in the group) and the rest of the users in the system.

#### Security Group

Creating this per region is very important as this decides the inbound and the outbound traffic in your instance's network.
For example you can only allow your SSH by whitelisting just your IP and specifying it for the SSH inbound rule.

Once you have created the IAM User, Security Group, now you can create your EC2 instance and attach these Groups and allow inbound & outbound traffic rules.

#### Static IP

1. [AWS Elastic IP](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html)
2. [Azure Reserved IP](https://azure.microsoft.com/en-us/blog/reserved-ip-addresses/)

Everytime the instance is shut down, its Public DNS IPv4 address will change, so to use a Static IP which will not change 
with the EC2 instance's IP, we use AWS Elastic IP address, which is called Reserved IP in Azure.
