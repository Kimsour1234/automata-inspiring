from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Lire le body brut du POST
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        # ---- Extraction des arrays ----
        prestations = data.get("Prestations", [])
        prix_ht = data.get("Prix HT", [])
        prix_ttc = data.get("Prix TTC", [])
        tva_percent = data.get("TVA %", [])
        montant_tva = data.get("Montant TVA", [])

        # ---- Formatage ----
        lignes = []
        for i in range(len(prestations)):
            nom = prestations[i]
            pu = prix_ht[i]
            qte = 1
            total = pu * qte
            lignes.append(f"{nom} – {qte} × {pu} € = {total} €")

        prestations_text = "\n".join(lignes)

        # ---- Totaux ----
        total_ht = sum(prix_ht)
        total_ttc = sum(prix_ttc)
        total_tva = sum(montant_tva)
        tva_unique = tva_percent[0] if tva_percent else 0

        result = {
            "LISTE_PRESTATIONS": prestations_text,
            "TOTAL_HT": total_ht,
            "TVA_POURCENT": tva_unique,
            "MONTANT_TVA": total_tva,
            "TOTAL_TTC": total_ttc
        }

        # ---- Réponse ----
        response_bytes = json.dumps(result).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response_bytes)


    def do_GET(self):
        # GET non autorisé
        self.send_response(405)
        self.end_headers()
