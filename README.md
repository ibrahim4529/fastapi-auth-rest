# fastapi-auth-rest
Simple and basic implementation auth on fast api
Using python-jose JWT

## Running
First clone this repo, after clone this repo run this command bellow

Install all deps
```bash
pip install -r requirements.txt
```
After installing all deps 
rename .env.example to .env and change the configuration
Run The app
```bash
uvicorn app.main:app --reload
```

## RUNNING USING DOCKER
You need install docker first

```bash
docker build --tag yourimagename .
```
```bash
docker run -d --name yourcontainername -p 8000:80 yourimagename
```

## OPEN APP
Open on your browser [http://localhost:8000](http://localhost:8000/docs).
