#dockerAPI

##Create copy of `web.env.default` as `web.env` and add Slack webhook url to web.env file

##Build and run containers
`cd app`
`docker-compose up --build`



##Test

`cd test`
`docker build --tag api-test .`
`docker run --network host api-test`
