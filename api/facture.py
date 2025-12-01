from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Lecture du body
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        body_str = raw_body.decode("utf-8")

        # Parse JSON (si ce n'est pas du JSON valide, on renvoie une erreur lisible)
        try:
            data = json.loads(body_str)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"Body non JSON : {body_str}".encode("utf-8"))
            return

        # 🔹 EXACTEMENT TES CLÉS JSON
        prestations   = data["Prestations"]
        prix_ht       = data["Prix HT"]
        prix_ttc      = data["Prix TTC"]
        tva_pourcent  = data["TVA %"]
        montant_tva   = data["Montant TVA"]

        # 🔹 Construction des lignes prestations
        lignes = []
        n = len(prestations)
        for i in range(n):
            nom = prestations[i]
            pu_ht = prix_ht[i] if i < len(prix_ht) else 0
            qte = 1
            total_ligne = pu_ht * qte
            lignes.append(f"{nom} – {qte} × {pu_ht} € = {total_ligne} €")

        liste_prestations = "\n".join(lignes)

        # 🔹 Totaux
        total_ht  = sum(prix_ht)
        total_ttc = sum(prix_ttc)
        total_tva = sum(montant_tva)
        tva_unique = tva_pourcent[0] if len(tva_pourcent) > 0 else 0

        # 🔹 JSON renvoyé à Make / Google Docs
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
