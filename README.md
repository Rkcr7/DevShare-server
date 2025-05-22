<p align="center">
  <img src="https://raw.githubusercontent.com/Rkcr7/DevShare/main/public/logo-big.png" width="150" alt="DevShare Logo"/>
</p>

<h1 align="center">DevShare Server</h1>

<p align="center">
  <a href="https://github.com/Rkcr7/DevShare-server/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Rkcr7/DevShare-server" alt="License"/>
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+"/>
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/flask-2.2.3-orange.svg" alt="Flask"/>
  </a>
</p>

<p align="center">
  <b>Transfer screenshots from your phone to your computer's clipboard instantly via Telegram</b>
</p>

<p align="center">
  The server component for <a href="https://github.com/Rkcr7/DevShare">DevShare</a> - a tool that enables instant screenshot transfer from your phone to your computer.
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-working-with-devshare-desktop-client">How It Works</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-deployment">Deployment</a> •
  <a href="#-api-endpoints">API</a> •
  <a href="#-usage-examples">Usage</a>
</p>

## 🚀 Features

- 🔄 **Seamless Integration**: Bridge between Telegram bot and desktop client
- 🖼️ **Screenshot Processing**: Handles images sent from mobile devices
- 🔒 **Secure Authentication**: Connection verification using Telegram IDs
- 📨 **Webhook Management**: Processes incoming Telegram messages
- 🌐 **Easy Deployment**: Quick setup on Railway's platform
- ⚡ **Realtime Sync**: Notifications when new screenshots arrive
- 📱 **Cross-Platform**: Works with Windows, macOS, and Linux clients

## 🔗 Working with DevShare Desktop Client

This server component works together with the [DevShare Desktop Client](https://github.com/Rkcr7/DevShare) to provide a complete screenshot sharing system:

### How it works

1. **Screenshot Flow**:
   - User takes a screenshot on their phone
   - User sends it to the DevShare Telegram bot
   - Server receives the image via Telegram webhook
   - Server notifies the connected desktop client
   - Desktop client fetches the image and copies it to clipboard
   - User can immediately paste the screenshot anywhere on their computer

2. **Connection Flow**:
   - Desktop client registers with server using user's Telegram ID
   - Server generates a unique connection ID for the client
   - Desktop client periodically pings the server to maintain connection
   - When a screenshot is sent to the bot, server notifies the connected client
   - Screenshots are delivered only to the authorized device

3. **Requirements**:
   - Both components (server and client) must be properly set up
   - User must provide their Telegram ID during client setup
   - Server must be publicly accessible with a proper webhook

## 🏗️ Architecture

The server has the following components:

1. **Flask Web Server**: Handles HTTP requests from both Telegram and desktop clients
2. **Webhook Handler**: Processes incoming screenshots from Telegram
3. **Client API**: Allows desktop applications to securely register and fetch screenshots
4. **In-memory Database**: Stores pending screenshots and client information

## 🔧 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- A Telegram Bot token (from [@BotFather](https://t.me/botfather))

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Rkcr7/DevShare-server.git
   cd DevShare-server
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Telegram bot token:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   ```

5. Run the server:
   ```bash
   python app.py
   ```

The server will be running at http://localhost:5000

## 🚀 Deployment

### Railway (Recommended)

Railway offers a simple deployment experience with a free tier:

1. Fork this repository to your GitHub account
2. Go to [Railway](https://railway.app/) and sign up/login with GitHub
3. Create a new project from your forked repository
4. Add the required environment variable:
   - `BOT_TOKEN` = your Telegram bot token
5. **Getting Your Public URL**:
   - After deployment is complete, go to the "Settings" tab
   - Navigate to "Networking" section
   - Select "Public Network" or "Public Domain"
   - Enter the port number (check deploy logs for the correct port, typically `8080`)
   - Railway will generate a public URL for your application
   - Copy this URL - you'll need it for the webhook setup and desktop client
6. Set up your Telegram bot webhook by adding bot token and webhook url in below url and you can open it in browser as well to setup:
   ```
   curl "https://api.telegram.org/bot<your_token>/setWebhook?url=https://<your-railway-url>/webhook"
   ```
7. To connect your desktop client, use the Railway URL when configuring the client's service URL

Alternatively, you can use the included deployment script:
```bash
python deploy_railway.py
```

For detailed deployment instructions, see the [DEPLOY.md](DEPLOY.md) file.

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page and server status |
| `/webhook` | POST | Telegram webhook handler for incoming messages |
| `/register` | POST | Register a new desktop client |
| `/ping` | POST | Client ping to maintain connection and check for new screenshots |
| `/fetch` | POST | Fetch pending screenshots for a client |
| `/set_commands` | GET | Set bot commands in Telegram |

## 🔌 Client Connection

DevShare desktop clients connect using the following flow:

1. **Registration**:
   - Client sends a request to `/register` with the user's Telegram ID
   - Server creates a unique connection ID and stores the mapping
   - Server returns the connection ID to the client

2. **Maintaining Connection**:
   - Client periodically sends requests to `/ping` with its connection ID
   - Server validates the connection and updates "last seen" timestamp
   - If a new screenshot is available, server notifies the client

3. **Receiving Screenshots**:
   - When notified of a new screenshot, client requests `/fetch`
   - Server provides the screenshot data in base64 format
   - Client decodes the image and copies it to clipboard

4. **Authentication**:
   - All connections are verified using the unique connection ID
   - Screenshots are only delivered to the authenticated device
   - If connection is invalid, client must re-register

## 📱 Usage Examples

### Setting Up with DevShare Desktop Client

1. Deploy this server to Railway
2. Configure the public URL in Railway's Networking settings:
   - Go to Settings > Networking
   - Select Public Network
   - Enter the port number (typically 8080, check deploy logs)
   - Get the generated public URL
3. Set up the webhook for your Telegram bot using the public URL
4. Download the setup [DevShare Desktop Client](https://github.com/Rkcr7/DevShare)
5. During client setup:
   - Enter your Telegram ID
   - If prompted for a service URL, enter the Railway public URL
6. The desktop client will automatically connect to your server
7. Send screenshots from your phone to the Telegram bot
8. Screenshots will appear on your desktop instantly!

### Use Cases

- **Web & Mobile Development**: Share mobile screenshots instantly with your development team
- **Design Reviews**: Transfer UI mockups from your phone to design tools
- **Remote Troubleshooting**: Help friends and family by receiving their device screenshots
- **AI & Development with Cursor**: Capture mobile content and paste directly into Cursor AI chat

## 🔐 Security

- All connections between client and server are secured with HTTPS
- Clients must provide a valid Telegram user ID to register
- Connection IDs are unique UUIDs that cannot be guessed
- Only the authenticated device can receive screenshots sent by the user

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Your Telegram Bot token | Yes |
| `PORT` | Port for the web server (default: 5000) | No |
| `LOG_LEVEL` | Logging level (default: INFO) | No |

## 👨‍💻 Development

Want to contribute to DevShare Server? Great! Here's how:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Commit your changes: `git commit -m "Add some feature"`
5. Push to the branch: `git push origin feature/my-feature`
6. Open a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to new functions and modules
- Write tests for new features
- Update documentation as needed

## ⚠️ Troubleshooting

- **Webhook Not Working**: Ensure your server is accessible from the internet and that you're using HTTPS
- **Bot Not Responding**: Check if your BOT_TOKEN is correct
- **Server Errors**: Check the application logs
- **Client Not Connecting**: Verify that you've entered the correct Telegram ID in the desktop client

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [DevShare Desktop Client](https://github.com/Rkcr7/DevShare) - The official desktop client for DevShare
- [Telegram Bot API](https://core.telegram.org/bots/api) - Documentation for the Telegram Bot API