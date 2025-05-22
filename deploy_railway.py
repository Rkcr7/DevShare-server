#!/usr/bin/env python
import os
import subprocess
import sys
import webbrowser
import requests
import json
import time

def run_command(command, silent=False):
    """Run a shell command and return its output and success status"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=False,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        if not silent:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"ERROR: {result.stderr}")
                
        return result.stdout, result.returncode == 0
    except Exception as e:
        if not silent:
            print(f"ERROR: {str(e)}")
        return "", False

def print_header(message):
    """Print a formatted header message"""
    print(f"\n>>> {message}")

def check_git():
    """Check if git is installed"""
    print_header("Checking if Git is installed")
    print("$ git --version")
    output, success = run_command("git --version")
    
    if not success or "git version" not in output.lower():
        print("Git not found! Please install Git from: https://git-scm.com/downloads")
        sys.exit(1)
    return True

def init_git_repo():
    """Initialize a git repository in the current directory"""
    print_header("Initializing git repository")
    
    # Check if .git already exists
    if os.path.exists(".git"):
        print("Git repository already initialized")
        return True
    
    print("$ git init")
    output, success = run_command("git init")
    
    return success

def commit_changes():
    """Commit all changes to git"""
    print_header("Committing changes")
    
    print("$ git add .")
    output, success = run_command("git add .")
    
    print("$ git commit -m \"Prepare for Railway deployment\"")
    output, success = run_command("git commit -m \"Prepare for Railway deployment\"")
    
    if "nothing to commit" in output:
        print("No changes to commit")
        return True
    
    return success

def setup_webhook(app_url, bot_token):
    """Set up the webhook for the Telegram bot"""
    print_header("Setting up webhook")
    
    webhook_url = f"{app_url}/webhook"
    api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}"
    
    print(f"Setting webhook to: {webhook_url}")
    
    # Use Python's requests library
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            print("Webhook set successfully!")
            print(response.text)
            return True
        else:
            print(f"Failed to set webhook: {response.text}")
            return False
    except Exception as e:
        print(f"Error setting webhook: {str(e)}")
        return False

def create_env_file(bot_token):
    """Create a .env file with the bot token"""
    print_header("Creating .env file for Railway")
    
    with open(".env", "w") as f:
        f.write(f"BOT_TOKEN={bot_token}\n")
    
    print("Created .env file with BOT_TOKEN")
    return True

def create_procfile():
    """Create a Procfile for Railway if it doesn't exist"""
    if not os.path.exists("Procfile"):
        print_header("Creating Procfile for Railway")
        
        with open("Procfile", "w") as f:
            f.write("web: gunicorn app:app\n")
        
        print("Created Procfile")
    else:
        print("Procfile already exists")
    
    return True

def verify_webhook(bot_token):
    """Verify that the webhook is set up correctly"""
    print_header("Verifying webhook")
    
    api_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            webhook_url = data.get('result', {}).get('url', '')
            print(f"Current webhook URL: {webhook_url}")
            print(f"Webhook status: {'✓ Active' if webhook_url else '✗ Not set'}")
            return bool(webhook_url)
        else:
            print(f"Failed to verify webhook: {response.text}")
            return False
    except Exception as e:
        print(f"Error verifying webhook: {str(e)}")
        return False

def open_railway_website():
    """Open Railway website for deployment"""
    print_header("Opening Railway website")
    
    railway_url = "https://railway.app/"
    webbrowser.open(railway_url)
    
    return True

def main():
    """Main deployment function"""
    print("=" * 60)
    print("DevShare Server - Railway Deployment Helper")
    print("=" * 60)
    print("\nThis script will help you deploy your DevShare server to Railway.")
    
    # Check prerequisites
    check_git()
    
    # Get bot token
    print_header("Enter your Telegram Bot Token")
    print("You can get this from the BotFather bot on Telegram (@BotFather)")
    bot_token = input("Bot Token: ").strip()
    
    if not bot_token:
        print("Bot token is required. Please restart the script and enter a valid token.")
        sys.exit(1)
    
    # Prepare files for Railway
    create_env_file(bot_token)
    create_procfile()
    
    # Initialize Git if needed
    init_git_repo()
    commit_changes()
    
    # Guide user through Railway deployment
    print_header("Railway Deployment Process")
    print("Follow these steps to deploy your DevShare server to Railway:\n")
    print("1. Create a GitHub repository for this project")
    print("   - Go to https://github.com/new")
    print("   - Name: DevShare-server")
    print("   - Description: Server component for the DevShare application")
    print("   - Choose public or private repository")
    print("   - Click 'Create repository'\n")
    
    print("2. Push your code to GitHub")
    print("   $ git remote add origin https://github.com/YOUR_USERNAME/DevShare-server.git")
    print("   $ git branch -M main")
    print("   $ git push -u origin main\n")
    
    print("3. Deploy on Railway")
    print("   - Sign up/log in to Railway with your GitHub account")
    print("   - Create a new project and select 'Deploy from GitHub repo'")
    print("   - Find and select your DevShare-server repository")
    print("   - Your app will be automatically deployed")
    print("   - Wait for the deployment to complete\n")
    
    proceed = input("Would you like to open the Railway website now? (y/n): ").strip().lower()
    if proceed == 'y':
        open_railway_website()
    
    print_header("Getting your Railway App URL")
    print("After deployment is complete:")
    print("1. Go to the 'Settings' tab in your Railway project")
    print("2. Look for the 'Networking' section")
    print("3. Select 'Public Network' or 'Public Domain'")
    print("4. Enter the port number from the deploy logs (typically 8080)")
    print("5. Railway will generate a public URL for your application")
    print("6. Copy this URL - you'll need it for the webhook setup and desktop client")
    
    app_url = input("\nEnter your app URL: ").strip()
    
    if app_url:
        # Make sure URL doesn't end with a slash
        if app_url.endswith('/'):
            app_url = app_url[:-1]
            
        # Set up the webhook
        setup_webhook(app_url, bot_token)
        
        # Verify the webhook
        time.sleep(2)  # Wait for webhook to propagate
        verify_webhook(bot_token)
        
        print_header("Deployment Complete!")
        print(f"Your DevShare server is now available at: {app_url}")
        print("To test it, send a message to your Telegram bot.")
        print("\nTo connect with the DevShare desktop client:")
        print(f"1. Enter your Telegram ID in the DevShare desktop app")
        print(f"2. The desktop app will automatically connect to your server")
        print(f"\nDesktop client repository: https://github.com/Rkcr7/DevShare")
    else:
        print("\nYou didn't provide an app URL. You can set up the webhook later with:")
        print(f"curl \"https://api.telegram.org/bot{bot_token}/setWebhook?url=YOUR_APP_URL/webhook\"")
    
    print("\n" + "=" * 60)
    print("Deployment preparation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main() 