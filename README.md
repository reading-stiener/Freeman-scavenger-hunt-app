# Freeman-scavenger-hunt-app
Web application built for a house event at Connecticut College. This application 
was built for mobile devices. The idea was to have 10 to 20 questions or riddles 
around a dorm that are accessible by QR codes. Logged in users could access the 
riddles by scanning the QR codes. 

The app is built on top of a flask server backend with an mySQL database. Because the
app is lean, it can easily be hosted on local machine using a service like ngrok. 

## Setting up the project
You need have a mySQL server tunning on the backend to host this project locally. 
Once that is set up, create a user account and set password. Next, edit the `config`
variable in app.py and game_logic.py to reflect user, password and host, port if 
applicable

Finally excute

```bash
python app.py 
```
to run the project on localhost.

## Hosting the project on the internet
You can use a service like ngrok to host localhost project on an exposed port.
