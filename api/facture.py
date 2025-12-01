from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        body_str = raw_body.decode("utf-8")

        data = json.loads(body_str)

        # ---- UTILISATION DES CLÉS EXACTES QUE MAKE ENVOIE ----
        prestations   = data["Prestations"]
        prix_ht       = data["Prix_HT"]
        prix_ttc      = data["Prix_TTC"]
        tva_percent   = data["TVA_%"]
        montant_tva   = data["Montant_TVA"]

        # ---- Lignes prestations ----
        lignes = []
        n = len(prestations)

        for i in range(n):
            nom = prestations[i]
            ht  = prix_ht[i]
            ttc = prix_ttc[i]
            lignes.append(f"- {nom} : {ht} € HT → {ttc} € TTC")

        liste_prestations = "\n".join(lignes)

        # ---- Totaux ----
        total_ht  = sum(prix_ht)
        total_ttc = sum(prix_ttc)
        total_tva = sum(montant_tva)
        tva_unique = tva_percent[0]

        result = {
            "LISTE_PRESTATIONS": liste_prestations,
            "TOTAL_HT": total_ht,
            "TVA_POURCENT": tva_unique,
            "MONTANT_TVA": total_tva,
            "TOTAL_TTC": total_ttc
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode("utf-8"))

    def do_GET(self):
        self.send_response(405)
        self.end_headers()
