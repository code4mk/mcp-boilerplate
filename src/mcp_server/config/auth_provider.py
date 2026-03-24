import os
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet
from fastmcp.server.auth.providers.github import GitHubProvider
from fastmcp.server.auth.providers.auth0 import Auth0Provider

def get_client_storage():
  """Get the client storage."""
  return FernetEncryptionWrapper(
    key_value=RedisStore(
      host=os.environ["REDIS_HOST"],
      port=int(os.environ["REDIS_PORT"]),
      password=os.environ.get("REDIS_PASSWORD"),
    ),
    fernet=Fernet(os.environ["STORAGE_ENCRYPTION_KEY"])
  )

def get_auth_provider(provider_name: str):
  """Get the auth provider based on the provider name."""
  if provider_name.lower() == "github":

    # Get GitHub configuration
    github_client_id = os.getenv("GITHUB_CLIENT_ID")
    github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
    base_url = os.getenv("RESOURCE_BASE_URL", "http://localhost:8000")    
    client_storage = get_client_storage()

    return GitHubProvider(
      client_id=github_client_id,
      client_secret=github_client_secret,
      base_url=base_url,

      # Production token management
      jwt_signing_key=os.environ["JWT_SIGNING_KEY"],
      client_storage=client_storage
    )
  elif provider_name.lower() == "auth0":

    auth0_domain = os.getenv("AUTH0_DOMAIN")
    auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
    auth0_client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    auth0_audience = os.getenv("AUTH0_AUDIENCE")
    base_url = os.getenv("RESOURCE_BASE_URL", "http://localhost:8000")
    client_storage = get_client_storage()

    auth0_config_url = f"https://{auth0_domain}/.well-known/openid-configuration"

    return Auth0Provider(
      config_url=auth0_config_url,
      client_id=auth0_client_id,
      client_secret=auth0_client_secret,
      audience=auth0_audience,
      base_url=base_url,
      required_scopes=["openid", "profile", "email"],

      jwt_signing_key=os.environ["JWT_SIGNING_KEY"],
      client_storage=client_storage
    )
  else:
    raise ValueError(f"Unsupported provider: {provider_name}")