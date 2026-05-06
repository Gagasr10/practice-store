from api.client import ApiClient


def get_invoices(token: str) -> dict:
    response = ApiClient(token=token).get("/invoices")
    response.raise_for_status()
    return response.json()


def get_invoice(invoice_id: str, token: str) -> dict:
    response = ApiClient(token=token).get(f"/invoices/{invoice_id}")
    response.raise_for_status()
    return response.json()


def create_invoice(payload: dict, token: str) -> dict:
    response = ApiClient(token=token).post("/invoices", json=payload)
    response.raise_for_status()
    return response.json()


def create_guest_invoice(payload: dict) -> dict:
    response = ApiClient().post("/invoices/guest", json=payload)
    response.raise_for_status()
    return response.json()


def update_invoice_status(invoice_id: str, status: str, token: str) -> dict:
    response = ApiClient(token=token).put(f"/invoices/{invoice_id}/status", json={"status": status})
    response.raise_for_status()
    return response.json()
