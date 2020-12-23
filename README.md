# ET DSS Tool 

A minimal working version of ET DSS using Docker, Flask and Heroku.

## Prerequisites:

- Docker
- Heroku CLI (only needed for deployment)
- VS Code + Docker Extension

## Steps 

Following are the steps for testing this app on Windows.

1. The first step requires the installation of Docker. The installer can be found [here](https://docs.docker.com/docker-for-windows/install/). 

2. Clone this repo: 

> `git clone https://github.com/eusojk/ET_DSS_hist`
> 
> `cd ET_DSS_hist`

3. From within the local repo, build the Dockerfile:

> `docker.exe build --tag et_dss_container .`

4. Then run the app locally:

> `docker run -p 5000:5000 et_dss_container --name "et_dss_app" `

5. For registering and deploying the app on Heroku:

> `heroku login`
>
> `heroku container:login`
>
> `heroku create et-dss-app1`
>
> `heroku container:push web --app et-dss-app1`
>
> `heroku container:release web --app et-dss-app1`