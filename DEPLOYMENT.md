# 🚀 Deployment Guide for Tricab Productivity App

## Deployment Options

### Option 1: Render (Full-Stack) - Recommended

#### Backend Deployment

1. **Create a Render account** at https://render.com

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Root Directory: `server`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Add Environment Variables**:
   ```
   SECRET_KEY=your-strong-secret-key-here
   DATABASE_URL=your-postgresql-url
   OPENAI_API_KEY=your-openai-key (optional)
   ```

4. **Create PostgreSQL Database**:
   - Create a new PostgreSQL database in Render
   - Copy the Internal Database URL
   - Add it as `DATABASE_URL` environment variable

5. **Update requirements.txt** (add gunicorn):
   ```bash
   echo "gunicorn==21.2.0" >> server/requirements.txt
   echo "psycopg2-binary==2.9.9" >> server/requirements.txt
   ```

#### Frontend Deployment

1. **Update API URL** in client code:
   - Create `client/src/config.js`:
   ```javascript
   export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5555';
   ```
   - Update fetch calls to use `${API_URL}/api/...`

2. **Deploy to Render**:
   - Create a new Static Site
   - Root Directory: `client`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `build`
   - Add Environment Variable: `REACT_APP_API_URL=https://your-backend.onrender.com`

---

### Option 2: Heroku

#### Backend

1. **Install Heroku CLI**:
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and create app**:
   ```bash
   heroku login
   cd server
   heroku create your-app-name
   ```

3. **Add PostgreSQL**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set OPENAI_API_KEY=your-openai-key
   ```

5. **Create Procfile** in server/:
   ```
   web: gunicorn app:app
   ```

6. **Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   heroku run flask db upgrade
   heroku run python seed.py
   ```

#### Frontend

Deploy to **Vercel** or **Netlify**:

**Netlify:**
```bash
cd client
npm run build
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

---

### Option 3: Railway

1. **Create Railway account**: https://railway.app

2. **New Project > Deploy from GitHub**

3. **Add PostgreSQL**: Click "New" > Database > PostgreSQL

4. **Configure Backend Service**:
   - Root Directory: `/server`
   - Start Command: `gunicorn app:app`
   - Add environment variables

5. **Configure Frontend Service**:
   - Root Directory: `/client`
   - Build Command: `npm install && npm run build`
   - Start Command: `npx serve -s build`

---

## Pre-Deployment Checklist

### Backend Changes

1. **Update app.py** for production:
   ```python
   # Change at the bottom of app.py
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5555))
       app.run(host='0.0.0.0', port=port, debug=False)
   ```

2. **Update CORS settings** in app.py:
   ```python
   CORS(app, 
        supports_credentials=True, 
        origins=['https://your-frontend-url.com', 'http://localhost:3000'])
   ```

3. **Add gunicorn** to requirements.txt:
   ```
   gunicorn==21.2.0
   psycopg2-binary==2.9.9
   ```

4. **Add runtime.txt** (optional):
   ```
   python-3.11.0
   ```

### Frontend Changes

1. **Create production API URL**:
   ```javascript
   // src/config.js
   export const API_URL = process.env.REACT_APP_API_URL || 
                          'https://your-backend.onrender.com';
   ```

2. **Update all fetch calls**:
   ```javascript
   import { API_URL } from './config';
   
   fetch(`${API_URL}/api/login`, { ... })
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

---

## Environment Variables

### Backend (.env)
```
SECRET_KEY=<strong-random-string>
DATABASE_URL=postgresql://user:pass@host:port/dbname
OPENAI_API_KEY=sk-...
FLASK_ENV=production
```

### Frontend (.env.production)
```
REACT_APP_API_URL=https://your-backend-url.com
```

---

## Database Migration on Production

After deploying backend:

```bash
# Render/Heroku
heroku run flask db upgrade
# or
railway run flask db upgrade

# Seed database (first time only)
heroku run python seed.py
```

---

## Post-Deployment Testing

1. ✅ Test signup and login
2. ✅ Create a project
3. ✅ Add tasks to project
4. ✅ Test CRUD operations
5. ✅ Verify authorization (can't access other users' data)
6. ✅ Test pagination
7. ✅ Test AI features (if configured)
8. ✅ Check dashboard statistics

---

## Monitoring & Maintenance

### Logs
```bash
# Heroku
heroku logs --tail

# Render
Check Render dashboard > Logs tab
```

### Database Backup
```bash
# Heroku
heroku pg:backups:capture
heroku pg:backups:download
```

### Update Application
```bash
git add .
git commit -m "Update message"
git push heroku main  # or push to GitHub for Render/Railway
```

---

## Troubleshooting

**Database Connection Issues:**
- Verify DATABASE_URL is set correctly
- Check if PostgreSQL addon is active
- Ensure psycopg2-binary is in requirements.txt

**CORS Errors:**
- Update CORS origins to include frontend URL
- Check credentials setting in CORS config

**Build Failures:**
- Check build logs for specific errors
- Verify all dependencies are in requirements.txt/package.json
- Ensure Python/Node versions are compatible

**Session Issues:**
- Set SECRET_KEY environment variable
- Configure session settings for production
- Check cookie domain settings

---

## Security Best Practices

1. ✅ Use strong SECRET_KEY
2. ✅ Use environment variables for all secrets
3. ✅ Enable HTTPS (automatic on most platforms)
4. ✅ Set secure cookie flags in production
5. ✅ Use PostgreSQL (not SQLite) in production
6. ✅ Keep dependencies updated
7. ✅ Enable database backups
8. ✅ Monitor error logs

---

## Cost Estimates

### Free Tier Options:
- **Render**: Free for web service + PostgreSQL (with limitations)
- **Heroku**: $5/month for hobby dyno + database
- **Railway**: $5/month credit (pay as you go)
- **Netlify/Vercel**: Free for frontend

### Recommended for Production:
- **Backend**: Render ($7/month) or Railway ($5-10/month)
- **Database**: Managed PostgreSQL ($7-10/month)
- **Frontend**: Netlify/Vercel (Free)
- **Total**: ~$15-20/month

---

## Domain Setup (Optional)

1. Purchase domain from Namecheap, Google Domains, etc.
2. Configure DNS in Render/Heroku/Railway dashboard
3. Update CORS settings with new domain
4. Update frontend API URL

---

**Your application is now live! 🎉**
