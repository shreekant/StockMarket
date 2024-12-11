import os
import requests

# Get environment variables
username = os.getenv('PYTHONANYWHERE_USERNAME')
api_token = os.getenv('PYTHONANYWHERE_API_TOKEN')

# Define the base URL for the PythonAnywhere API
base_url = f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{username}/stock-market/'

# Define the headers for the API requests
headers = {
    'Authorization': f'Token {api_token}'
}

# Function to upload a file to PythonAnywhere
def upload_file(local_path, remote_path):
    with open(local_path, 'rb') as file_content:
        response = requests.post(
            base_url + remote_path,
            headers=headers,
            files={'content': file_content}
        )
    if response.status_code == 201:
        print(f'Successfully uploaded {local_path} to {remote_path}')
    else:
        print(f'Failed to upload {local_path} to {remote_path}: {response.content}')

# Walk through the local directory and upload all files
for root, dirs, files in os.walk('.'):
    for file in files:
        local_path = os.path.join(root, file)
        remote_path = os.path.relpath(local_path, '.')
        upload_file(local_path, remote_path)