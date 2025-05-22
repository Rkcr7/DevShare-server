# DevShare Server Deployment Guide

This guide covers the deployment options for the DevShare server.

## Table of Contents

- [Railway Deployment (Recommended)](#railway-deployment-recommended)
- [Setting Up Telegram Webhooks](#setting-up-telegram-webhooks)
- [Verifying Your Deployment](#verifying-your-deployment)
- [Environment Variables](#environment-variables)
- [Manual Deployment](#manual-deployment)

## Railway Deployment (Recommended)

Railway is the simplest hosting platform for deploying the DevShare server. It offers a generous free tier and seamless GitHub integration.

### Steps:

1. **Create a Railway Account**
   - Go to [Railway](https://railway.app)
   - Sign up with your GitHub account

2. **Create a new Project**
   - Click on "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account if not already connected
   - Select your forked DevShare-server repository

3. **Configure Environment Variables**
   - Go to the "Variables" tab
   - Add `BOT_TOKEN` with your Telegram bot token value
   
4. **Deploy**
   - Railway will automatically deploy your app
   - Once deployed, go to the "Settings" tab to find your app's URL
   
5. **Configure Public URL**
   - In the "Settings" tab, navigate to the "Networking" section
   - Select "Public Network" or "Public Domain"
   - You need to specify the port number your application is using
   - Check the deploy logs for the port number (typically `8080`)
   - Enter this port number in the configuration
   - Railway will generate a public URL for your application
   - This is the URL you'll use for both the webhook setup and desktop client configuration
   
6. **Set Up Webhook**
   - Use the URL from the Networking section to set up your Telegram webhook
   - Follow the webhook setup instructions in the section below

## Setting Up Telegram Webhooks

After deployment, you need to tell Telegram where to send incoming messages:

### For Railway:
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_RAILWAY_APP_URL>/webhook"
```

### For Custom Domains:
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_DOMAIN>/webhook"
```

## Verifying Your Deployment

To verify that your deployment is working correctly:

1. **Check Webhook Status**
   ```bash
   curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
   ```
   You should see your webhook URL and that it's active.

2. **Visit the Home Page**
   Open your browser and navigate to your app's URL. You should see the DevShare server homepage.

3. **Test with Telegram**
   Send a message to your bot on Telegram. If everything is set up correctly, your bot should respond.

4. **Connect with Desktop Client**
   - Download the [DevShare Desktop Client](https://github.com/Rkcr7/DevShare)
   - Enter your Telegram ID during setup
   - If the connection is established successfully, you're ready to go!

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Your Telegram Bot token | Yes |
| `PORT` | Port for the web server (default: 5000) or 8080 | No | check railway logs for the port
| `LOG_LEVEL` | Logging level (default: INFO) | No |

## Manual Deployment

For advanced users who want to deploy on their own infrastructure.

### Prerequisites:
- Linux server with Python 3.9+
- Nginx or Apache web server
- Domain name (optional but recommended)

### Steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Rkcr7/DevShare-server.git
   cd DevShare-server
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

3. **Create Environment File**
   ```bash
   echo "BOT_TOKEN=your_telegram_bot_token" > .env
   ```

4. **Set Up Systemd Service**
   Create a systemd service file at `/etc/systemd/system/devshare.service`:
   ```
   [Unit]
   Description=DevShare Telegram Bot Server
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/DevShare-server
   ExecStart=/path/to/DevShare-server/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
   Restart=always
   Environment="PYTHONPATH=/path/to/DevShare-server"
   EnvironmentFile=/path/to/DevShare-server/.env

   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure Nginx**
   ```
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

6. **Enable and Start Services**
   ```bash
   sudo systemctl enable nginx
   sudo systemctl start nginx
   sudo systemctl enable devshare
   sudo systemctl start devshare
   ```

7. **Set Up HTTPS with Let's Encrypt (Recommended)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your_domain.com
   ```

## Troubleshooting

- **Webhook Not Working**: Ensure your server is accessible from the internet and that you're using HTTPS
- **Bot Not Responding**: Check if your BOT_TOKEN is correct
- **Server Errors**: Check the application logs
- **Client Not Connecting**: Verify that you've entered the correct Telegram ID in the desktop client 