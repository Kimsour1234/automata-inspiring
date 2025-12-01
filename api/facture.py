from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        data = json.loads(body)

        prestations   = data["Prestations"]
        prix_ht       = data["Prix_HT"]
        prix_ttc      = data["Prix_TTC"]
        tva_percent   = data["TVA_%"]
        montant_tva   = data["Montant_TVA"]

        lignes = []
        for i in range(len(prestations)):
            nom = prestations[i]
            ht  = prix_ht[i]
            ttc = prix_ttc[i]
            lignes.append(f"- {nom} : {ht} € HT → {ttc} € TTC")

        liste_prestations = "\n".join(lignes)

        result = {
            "LISTE_PRESTATIONS": liste_prestations,
            "TOTAL_HT": sum(prix_ht),
            "TVA_POURCENT": tva_percent[0] if tva_percent else 0,
            "MONTANT_TVA": sum(montant_tva),
            "TOTAL_TTC": sum(prix_ttc)
        }

        res = json.dumps(result).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(res)

    def do_GET(self):
        self.send_response(405)
        self.end_headers()
