from http.server import BaseHTTPRequestHandler
import json
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('content-length', 0))
            data = json.loads(self.rfile.read(length))
            raw = str(data.get("number", "")).strip()
            
            if not raw.startswith('+'):
                raw = '+' + raw.lstrip('+')
            
            parsed = phonenumbers.parse(raw)
            
            result = {
                "success": True,
                "valid": phonenumbers.is_valid_number(parsed),
                "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "local": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                "country": geocoder.description_for_number(parsed, "en"),
                "carrier": carrier.name_for_number(parsed, "en") or "Unknown",
                "countryCode": parsed.country_code,
                "timezone": timezone.time_zones_for_number(parsed),
                "type": "Mobile" if phonenumbers.number_type(parsed) == 1 else "Fixed Line / Other"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())
            
        except Exception:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "bad number - use full international format like +91xxxxxxxxxx"}).encode())
