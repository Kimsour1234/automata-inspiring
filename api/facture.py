from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Lecture du body
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        body_str = raw_body.decode("utf-8")

        # Parse JSON propre
        data = json.loads(body_str)

        # ---- TES CLÉS EXACTES ----
        prestations   = data["Prestations"]
        prix_ht       = data["Prix HT"]
        prix_ttc      = data["Prix TTC"]
        tva_percent   = data["TVA %"]
        montant_tva   = data["Montant TVA"]

        # ---- Lignes prestations ----
        lignes = []
        n = len(prestations)

        for i in range(n):
            nom = prestations[i]
            ht  = prix_ht[i] if i < len(prix_ht) else 0
            ttc = prix_ttc[i] if i < len(prix_ttc) else 0
            lignes.append(f"- {nom} : {ht} € HT → {ttc} € TTC")

        liste_prestations = "\n".join(lignes)

        # ---- Totaux ----
        total_ht  = sum(prix_ht)
        total_ttc = sum(prix_ttc)
        total_tva = sum(montant_tva)
        tva_unique = tva_percent[0] if len(tva_percent) > 0 else 0

        # ---- Résultat renvoyé à Make ----
        result = {
            "LISTE_PRESTATIONS": liste_prestations,
            "TOTAL_HT": total_ht,
            "TVA_POURCENT": tva_unique,
            "MONTANT_TVA": total_tva,
            "TOTAL_TTC": total_ttc
        }

        res_bytes = json.dumps(result).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(res_bytes)

    def do_GET(self):
        self.send_response(405)
        self.end_headers()
