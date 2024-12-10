import subprocess

# Define the command and its arguments
command = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
arguments = r'--remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"'

# Execute the command and keep the browser open
subprocess.Popen(f'{command} {arguments}', shell=True)
print("Chrome started with remote debugging.")