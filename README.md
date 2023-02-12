# huttustutka

[huttustutka](https://huttusta.rotta.gt)

## backend
```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
flask run
```

## frontend
```
cd front
npm i
touch .env
echo "VITE_GOOGLE_API_KEY=your-key" >> .env
echo "VITE_API_URL=http://127.0.0.1:5000" >> .env
npm run dev
```

## tuotanto

```
docker run -d --name back huttustutka-back
docker run -v /etc/letsencrypt/archive/huttusta.rotta.gt:/etc/nginx/certs -d --name front -p 80:80 -p 443:443 huttustutka-front
```
