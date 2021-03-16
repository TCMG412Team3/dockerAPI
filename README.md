dockerAPI


#Build image

`docker build --tag python-docker .`


#Run container

`docker run -p 5000:5000 -e WEBHOOK_URL="<WEBHOOK_URL>" python-docker`
