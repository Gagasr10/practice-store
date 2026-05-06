"""E02 — TOTP two-factor authentication."""
import uuid
import pytest

from api.client import ApiClient
import api.auth as auth_api


@pytest.mark.edge
@pytest.mark.api
def test_totp_setup_and_login():
    """Verify the TOTP setup endpoint returns a valid secret structure.

    Uses a throwaway registered user so that enabling TOTP does not affect
    shared test accounts. Full TOTP login flow (generate code → verify) requires
    the pyotp library and is out of scope here.
    """
    client = ApiClient()
    unique_email = f"totp_{uuid.uuid4().hex[:8]}@example.com"
    unique_pwd = f"Tr3stT0tp_{uuid.uuid4().hex[:6]}!"
    reg = client.post("/users/register", json={
        "first_name": "TOTP", "last_name": "Test",
        "email": unique_email, "password": unique_pwd,
        "password_confirmation": unique_pwd,
    })
    if reg.status_code not in (200, 201):
        pytest.skip(f"Could not register throwaway user for TOTP test: {reg.text[:100]}")

    token = auth_api.login(unique_email, unique_pwd)["access_token"]
    auth_client = ApiClient(token=token)

    setup_resp = auth_client.post("/totp/setup", json={})
    assert setup_resp.status_code in (200, 201), (
        f"TOTP setup returned unexpected status {setup_resp.status_code}"
    )
    setup_data = setup_resp.json()
    assert (
        "secret" in setup_data
        or "qr_code" in setup_data
        or "totp_secret" in setup_data
        or "qrCodeUrl" in setup_data
    ), f"TOTP setup response missing expected fields: {setup_data}"
