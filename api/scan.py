from http.server import BaseHTTPRequestHandler
import json
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import random

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('content-length', 0))
            data = json.loads(self.rfile.read(length))
            raw = str(data.get("number", "")).strip()
            if not raw.startswith('+'):
                raw = '+' + raw.lstrip('+')
            
            parsed = phonenumbers.parse(raw)
            num = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            clean_num = num.replace('+', '')
            
            result = {
                "success": True,
                "basic": {
                    "valid": phonenumbers.is_valid_number(parsed),
                    "e164": num,
                    "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                    "local": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                    "country": geocoder.description_for_number(parsed, "en"),
                    "carrier": carrier.name_for_number(parsed, "en") or "Unknown",
                    "countryCode": parsed.country_code,
                    "timezone": timezone.time_zones_for_number(parsed),
                    "type": "Mobile" if phonenumbers.number_type(parsed) == 1 else "Fixed Line"
                },
                "osint": {
                    "google_dorks": [
                        f"https://google.com/search?q=%22{num}%22",
                        f"https://google.com/search?q=site:facebook.com+intext:{clean_num}",
                        f"https://google.com/search?q=site:truecaller.com+{clean_num}",
                        f"https://google.com/search?q=site:whatsapp.com+{clean_num}"
                    ],
                    "reputation": random.choice(["Clean", "Spam reports: 7", "Scam linked", "Debt collector"]),
                    "disposable": random.choice(["No", "Possible VoIP / Temp number"]),
                    "social": f"Found mentions on {random.randint(3,15)} platforms (FB, IG, Twitter, etc.)",
                    "leaks": random.choice(["No known leaks", "Appears in 2 data breaches"]),
                    "location_hint": geocoder.description_for_number(parsed, "en")
                },
                "warning": "This is simulated OSINT data for demonstration. Real investigations require legal tools.",
                "scan_time": "0.8s"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result, indent=2).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid number. Use full international format (+country code)"}).encode())
