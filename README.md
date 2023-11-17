# capstone-project-3900f11adusm

## Getting Started

This Web Application is meant to be run on unix based systems, such as MacOS or Linux. The application itself
is ran within docker containers. It is possible to configure the build to be able to run on Windows and other
systems, but the build tools for the docker containers are designed to be run on a unix based system.

### Prerequisites

Before building the docker images and producing docker containers, we must first have the Docker desktop application
installed on our device.

* Docker Desktop Application [Download Page](https://www.docker.com/products/docker-desktop/)

Make sure to have the correct version of the Docker Desktop Application installed, appropriate towards your client.


### Setup

_The below instructions are outlined under the basis that the commands will be run in the root folder of this project._

From here, there are two methods to setup of the Web Application. First is through the Makefile and managing the
Web Application through the Makefile.

1. First run the make build command. This will build the application. Though initial compilation will take some time.
    ```sh 
    make build
    ```

2. Afterwards, in your browser go to [http://localhost:3000/](http://localhost:3000/). This is main route to open the Web 
    Application.

3. Pressing `Ctrl-C` in the terminal will stop the application.


The second method is to manually build the docker containers through your terminal.

1. From the root directory of the project, run the following command:
    ```sh
    docker compose down && docker compose up --build
    ```

2. Afterwards, in your browser go to [http://localhost:3000/](http://localhost:3000/). This is main route to open the Web 
    Application.

3. Pressing `Ctrl-C` in the terminal will stop the application.


### Other Makefile commands

1. To remove the docker containers we can run: 
    ```sh
    make down
    ```

2. To kill the Web Application we can run:
    ```sh
    make kill
    ```

3. The following command will populate the Web Application with pre-organised data.
    ```sh 
    make populate
    ``` 

4. Finally, the below two commands will remove images and volumes.
    ```sh
    make remove_images
    make remove_volumes
    ```


## Usage 

Simply initialising the Web Application would start it at the bare minimum. As such, we recommend that, after running 
```make build``` you run ```make populate```. 

This will populate the application with some accounts and other resources such as campaigns, collectibles in the campaigns
and etc. You will also have access to the following accounts.
```
email: sz@gmail.com password: stella - Manager Account
email: ua@gmail.com password: uguudei - Admin Account
email: ds@gmail.com password: dyllanson - Admin Account
email: mx@gmail.com password: meng - Collector Account
email: gw@gmail.com password: greg - Collector Account
```











<p align="right">(<a href="#readme-top">back to top</a>)</p>