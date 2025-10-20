import time
import jwt
import requests
import os

def set_github_access_token_from_env(
    app_id_env: str, 
    secret_key_env: str, 
    installation_id_env: str | None = None
) -> str:
    """Generate a GitHub App installation access token using environment variables.
    
    If installation_id_env is not provided or the environment variable is not set,
    the function will automatically fetch the first available installation for the app.
    
    Args:
        app_id_env: Environment variable name containing the GitHub App ID
        secret_key_env: Environment variable name containing the private key (PEM format)
        installation_id_env: Optional environment variable name containing the installation ID.
                           If None or not set, will use the first available installation.
        
    Returns:
        The access token
    """
    app_id = os.environ.get(app_id_env)
    secret_key = os.environ.get(secret_key_env)
    
    if not app_id:
        raise ValueError(f"Environment variable {app_id_env} is not set")
    if not secret_key:
        raise ValueError(f"Environment variable {secret_key_env} is not set")
    
    # Handle newlines in private key if stored as escaped string
    if '\\n' in secret_key:
        secret_key = secret_key.replace('\\n', '\n')

    payload = {
        # Issued at time
        'iat': int(time.time()),
        # JWT expiration time (10 minutes maximum)
        'exp': int(time.time()) + 600,
        # GitHub App's client ID
        'iss': app_id
    }

    # Create JWT using RS256 for GitHub App authentication
    encoded_jwt = jwt.encode(payload, secret_key, algorithm='RS256')

    # Get installation ID if not provided
    installation_id = None
    if installation_id_env:
        installation_id = os.environ.get(installation_id_env)
    
    if not installation_id:
        # Fetch all installations for this app
        headers = {
            'Authorization': f'Bearer {encoded_jwt}',
            'Accept': 'application/vnd.github.v3+json',
        }
        installations_response = requests.get(
            'https://api.github.com/app/installations',
            headers=headers,
            timeout=30,
        )
        installations_response.raise_for_status()
        installations = installations_response.json()
        
        if not installations:
            raise ValueError("No installations found for this GitHub App")
        
        # Use the first installation
        installation_id = installations[0]['id']
        print(f"Using installation ID: {installation_id} (account: {installations[0]['account']['login']})")

    # Request an installation access token
    headers = {
        'Authorization': f'Bearer {encoded_jwt}',
        'Accept': 'application/vnd.github.v3+json',
    }
    response = requests.post(
        f'https://api.github.com/app/installations/{installation_id}/access_tokens',
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    token_data = response.json()
    
    access_token = token_data['token']
    print(f"GitHub access token obtained successfully for installation {installation_id}.")
    os.environ["GITHUB_APP_TOKEN"] = access_token
    
    return access_token


def get_github_access_token_from_pem(
    pem: str, client_id: str,
) -> str:
    """Generate a GitHub App installation access token using a JWT."""

    with open(pem, 'rb') as pem_file:
        signing_key = pem_file.read()

    payload = {
        # Issued at time
        'iat': int(time.time()),
        # JWT expiration time (10 minutes maximum)
        'exp': int(time.time()) + 600,
        # GitHub App's client ID
        'iss': client_id
    }

    # Create JWT
    encoded_jwt = jwt.encode(payload, signing_key, algorithm='RS256')
    return encoded_jwt
