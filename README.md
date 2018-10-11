# SpotifyPythonControl

## Requirements
    Python 3.6 or greater
    Spotify Premium

# Installation 
 
 ## Step 1
 - Clone the repository ` git clone https://github.com/amahlaka/SpotifyPythonControl.git`

 - ### Setting up the Virtual enviroment
```
cd SpotifyPythonControl
python3.x -m venv venv
```
### Activate the virtual enviroment
 
Powershell: ```.\venv\Scripts\Activate.ps1 ```  
Commandline: ```.\venv\Scripts\activate.bat```  
Linux Bash: ```source venv/bin/activate ``` 

### Install requirements
`pip install -r requirements.txt`

### Config
 - You need to have spotify API keys from [here](https://developer.spotify.com/dashboard/)
 - Paste your Client ID and Client Secret to [config.py](config.py)
 - Run `python flask_secret_generator.py` and copy output to [\_\_init\_\_.py](app/__init__.py) on the `app.secret_key` variable
 - Save both files
 - Start server with: `python .\wsgi.py`

 This should start a webserver at [127.0.0.1:5000](http://127.0.0.1:5000)  
 On the page you should see a button "Login", click that to authenticate with spotify.  
 You are then shown a list of devices that you have your account active on  
 Select the one you want to control


 