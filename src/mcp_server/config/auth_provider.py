import os
from fastmcp.server.auth.providers.github import GitHubProvider

def get_auth_provider(provider_name: str):
  """Get the auth provider based on the provider name."""
  if provider_name.lower() == "github":
    return GitHubProvider(
      client_id=os.getenv("GITHUB_CLIENT_ID"),
      client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
      base_url=os.getenv("RESOURCE_BASE_URL"),
    )
  else:
    raise ValueError(f"Unsupported provider: {provider_name}")