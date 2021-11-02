# diera-prod
Website of the cultural center Diera do sveta

## Set-up

### Deployment on PythonAnywhere

Following [the
instructions](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject)
on [PythonAnywhere help pages](https://help.pythonanywhere.com):

#### Upload the code to PythonAnywhere

Init: ```git clone https://github.com/mar-vic/diera-prod.git```

Update: ```git pull origin main```

#### Create virtual environment and install requirements

```
$ mkvirtualenv --python=/usr/bin/python3.8 diera
(diera)$ pip install -r requirements.txt
```

#### Set-up the web app and WSGI file

#### Set-up database

In settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<user>$<database>',
        'USER': '<user>,
        'PASSWORD': '<password>,
        'HOST': '<user>.mysql.eu.pythonanywhere-services.com',
     }
}
```

#### Set-up static files serving

