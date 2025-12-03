from http.server import BaseHTTPRequestHandler
import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build


# ---- Initialisation globale (une fois au cold start) ----
SERVICE_ACCOUNT_JSON = os.environ["GOOGLE_SERVICE_ACCOUNT_KEY"]
PARENT_FOLDER_ID = os.environ["GOOGLE_PARENT_DRIVE_ID"]

creds_info = json.loads(SERVICE_ACCOUNT_JSON)

creds = service_account.Credentials.from_service_account_info(
    creds_info,
    scopes=["https://www.googleapis.com/auth/drive"]
)

drive = build("drive", "v3", credentials=creds)


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            # Lire le body JSON venant de Make
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length).decode("utf-8") or "{}"
            data = json.loads(raw_body)

            # Nom du dossier à créer
            folder_name = data.get("folder_name", "test")

            file_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [PARENT_FOLDER_ID],
            }

            folder = drive.files().create(
                body=file_metadata,
                fields="id, name"
            ).execute()

            response_body = {
                "status": "success",
                "folder_id": folder["id"],
                "folder_name": folder["name"],
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(response_body).encode("utf-8"))

        except Exception as e:
            # Retourner l’erreur à Make pour debug
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e),
            }).encode("utf-8"))

    def do_GET(self):
        # On bloque GET
        self.send_response(405)
        self.end_headers()
