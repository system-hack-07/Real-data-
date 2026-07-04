from http.server import BaseHTTPRequestHandler
import json, phonenumbers
from phonenumbers import geocoder, carrier

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            p = phonenumbers.parse(data['number'])
            res = {
                "valid": phonenumbers.is_valid_number(p),
                "e164": phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164),
                "country": geocoder.description_for_number(p, "en"),
                "carrier": carrier.name_for_number(p, "en") or "N/A"
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
        except:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error":"bad number"}).encode())
