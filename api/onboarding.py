from http.server import BaseHTTPRequestHandler
import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            # --- lire le body JSON ---
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            nom_dossier = data.get("folder_name", "test")

            # --- récupérer les variables d'environnement ---
            service_email = os.environ["GOOGLE_SERVICE_ACCOUNT_EMAIL"]
            private_key = os.environ["GOOGLE_SERVICE_ACCOUNT_KEY"].replace("\\n", "\n")
            parent_id = os.environ["GOOGLE_PARENT_DRIVE_ID"]

            creds_info = {
                "type": "service_account",
                "client_email": service_email,
                "private_key": private_key,
                "token_uri": "https://oauth2.googleapis.com/token",
            }

            creds = service_account.Credentials.from_service_account_info(
                creds_info,
                scopes=["https://www.googleapis.com/auth/drive"],
            )

            drive = build("drive", "v3", credentials=creds)

            # --- créer le dossier dans Drive ---
            file_metadata = {
                "name": nom_dossier,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_id],
            }

            folder = drive.files().create(body=file_metadata, fields="id").execute()
            folder_id = folder.get("id")

            # --- réponse ---
            resp = {
                "status": "success",
                "folder_id": folder_id,
                "folder_name": nom_dossier,
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def do_GET(self):
        self.send_response(405)
        self.end_headers()
