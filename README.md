# petRock
## How To setup Docker For Development
Download Docker Desktop use plan free or paid if you wanna spend $$$<br>

### 1. clone repo from github to your device
In terminal cd into the folder you want to clone into:
```
git clone <link>
```

### 2. Build Docker image (now that you have repo)
> [!NOTE]
> You need to have Docker Desktop open, if not you will recieve and error and it will not build.

1. cd into the petRock folder/directory 
```
cd path/to/petRock
```
<br>

> [!IMPORTANT]
> There is another way to run it that will automatically update everytime it is built. This way I mentioned here makes it so that each time a change is made, you have to build, delete, hen run again to see changes. For the other way, scip till "Running with Compose."

2. Build Docker image using this command
```
docker build -t petrock .
```
* -t petrock tags your image with the name "petrock."
* The final . tells Docker to use the current directory (which contains the Dockerfile) as the build context

### 3. Run the container without Compose
Once the image is build you can run it with:
```
docker run -d -p 80:80 --name petrock-container petRock
```
* -d runs the container in detached mode
* -p 80:80 maps port 80 of your local machine to port 80 of the container
* --name petrock-container assigns a name to your running container
* petRock is the image name we built

### View page
Go to your Docker Desktop and click on the port 80:80 or navigate to http://localhost

You should now see the website hosted by NGINX.

To stop the container, you can either type:
```
docker stop petrock-container
docker rm petrock-container
```
* rm removes the container named "petrock-container" from your system and fress up system resources.

Or you can do it through Docker Desktop and just click the pause button and trashcan button.

## Run the container WITH Compose
Instead of doing docker run -d..., do this command:
```
docker-compose up --build -d
```
How it works:
1. Make any chages to files or Dockerfile
2. Run the command
command:
```
docker-compose up --build -d
```
3. Visit your app at http://localhost or throguh Docker Desktop app
4. When done:
```
docker-compose down
```
or delete it through app.

