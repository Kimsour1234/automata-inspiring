from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Lire le body brut
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        # ---- extraction des arrays ----
        prestations = data.get("Prestations", [])
        prix_ht = data.get("Prix HT", [])
        prix_ttc = data.get("Prix TTC", [])
        tva_percent = data.get("TVA %", [])
        montant_tva = data.get("Montant TVA", [])

        # ---- formatage des lignes prestation ----
        lignes = []
        for i in range(len(prestations)):
            nom = prestations[i]
            pu = prix_ht[i]
            qte = 1
            total = pu * qte
            lignes.append(f"{nom} – {qte} × {pu} € = {total} €")

        prestations_text = "\n".join(lignes)

        # ---- totaux ----
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

        # ---- réponse ----
        response_bytes = json.dumps(result).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response_bytes)

    # Pour éviter l’erreur 405 GET
    def do_GET(self):
        self.send_response(405)
        self.end_headers()

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
