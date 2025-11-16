from typing import Tuple, Dict, Optional
import logging

from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import AzureError
logger = logging.getLogger(__name__)


Keyvaultname = "dataSchemeExtractorKV"

def fetch_secrets_from_keyvault(
    vault_url: str,
    secret_names: Tuple[str, str],
    managed_identity_client_id: Optional[str] = None,
) -> Dict[str, str]:
    """
    Fetch secrets AAA and BBB from an Azure Key Vault using Managed Identity.

    Parameters
    ----------
    vault_url:
        Full Key Vault URL, e.g. "https://<your-vault-name>.vault.azure.net"
    secret_names:
        Tuple of two secret names to fetch (defaults to ("AAA", "BBB")).
    managed_identity_client_id:
        If using a user-assigned managed identity, pass its client id here.
        If None, DefaultAzureCredential is used and will pick up the environment / system-assigned identity.

    Returns
    -------
    dict
        Mapping {secret_name: secret_value}

    Raises
    ------
    RuntimeError on failure to retrieve any secret (wraps Azure errors).
    """
    if len(secret_names) != 2:
        raise ValueError("secret_names must be a tuple of two names (AAA, BBB).")

    # Choose credential:
    # - If user provides a managed_identity_client_id, use ManagedIdentityCredential explicitly.
    # - Otherwise DefaultAzureCredential will attempt managed identity in Azure environment.
    if managed_identity_client_id:
        credential = ManagedIdentityCredential(client_id=managed_identity_client_id)
    else:
        credential = DefaultAzureCredential()

    client = SecretClient(vault_url=vault_url, credential=credential)

    results: Dict[str, str] = {}
    try:
        for name in secret_names:
            logger.debug("Fetching secret %s from Key Vault %s", name, vault_url)
            secret = client.get_secret(name)
            results[name] = secret.value
        return results

    except AzureError as az_err:
        # AzureError covers network/auth/authorization/404 etc.
        logger.exception("Failed to fetch secrets from Key Vault: %s", az_err)
        raise RuntimeError(f"Error fetching secrets from Key Vault: {az_err}") from az_err