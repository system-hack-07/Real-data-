from http.server import BaseHTTPRequestHandler
import json
import phonenumbers
from phonenumbers import geocoder, carrier

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('content-length', 0))
            if length == 0:
                raise ValueError("No data")
                
            data = json.loads(self.rfile.read(length))
            raw = data.get("number", "").strip()
            
            if not raw:
                raise ValueError("Empty number")
            
            parsed = phonenumbers.parse(raw)
            
            result = {
                "valid": phonenumbers.is_valid_number(parsed),
                "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "local": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                "country": geocoder.description_for_number(parsed, "en"),
                "carrier": carrier.name_for_number(parsed, "en") or "Unknown",
                "countryCode": parsed.country_code
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "bad number or invalid format"}).encode())
