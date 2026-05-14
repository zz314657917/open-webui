import os
from typing import Optional

from open_webui.models.users import UserModel
from open_webui.utils.oauth import decrypt_data


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def _trim_slash(value: str) -> str:
    return value.strip().rstrip('/')


SUB2API_SSO_ENABLED = _env_bool('SUB2API_SSO_ENABLED', True)
SUB2API_BASE_URL = _trim_slash(os.environ.get('SUB2API_BASE_URL', 'http://127.0.0.1:62080'))
SUB2API_REDEEM_URL = os.environ.get(
    'SUB2API_REDEEM_URL',
    f'{SUB2API_BASE_URL}/api/v1/internal/open-webui/redeem',
).strip()
SUB2API_REDEEM_SECRET = os.environ.get('SUB2API_REDEEM_SECRET', '').strip()
SUB2API_LAUNCH_URL = os.environ.get(
    'SUB2API_LAUNCH_URL',
    f'{SUB2API_BASE_URL}/open-webui/launch',
).strip()


def get_sub2api_public_config() -> dict:
    return {
        'enabled': SUB2API_SSO_ENABLED,
        'launch_url': SUB2API_LAUNCH_URL,
    }


def redact_sub2api_info(info: Optional[dict]) -> Optional[dict]:
    if not isinstance(info, dict):
        return info
    if 'sub2api' not in info:
        return info
    return {
        **info,
        'sub2api': {
            'configured': bool(info.get('sub2api')),
        },
    }


def get_user_sub2api_binding(user: Optional[UserModel]) -> Optional[dict]:
    if not user or not getattr(user, 'settings', None):
        return None

    settings = user.settings
    if hasattr(settings, 'model_dump'):
        settings = settings.model_dump()
    elif not isinstance(settings, dict):
        return None

    binding = settings.get('sub2api')
    if not isinstance(binding, dict):
        return None

    if not binding.get('enabled', True):
        return None

    gateway_base_url = binding.get('gateway_base_url')
    if not gateway_base_url:
        return None

    info = getattr(user, 'info', None) or {}
    secrets = info.get('sub2api') if isinstance(info, dict) else None
    encrypted_api_key = secrets.get('api_key_encrypted') if isinstance(secrets, dict) else None
    if not encrypted_api_key:
        return None

    try:
        secret_data = decrypt_data(str(encrypted_api_key))
    except Exception:
        return None

    api_key = secret_data.get('api_key') if isinstance(secret_data, dict) else None
    if not api_key:
        return None

    return {
        **binding,
        'api_key': str(api_key),
        'gateway_base_url': _trim_slash(str(gateway_base_url)),
    }
