import requests
import traceback
import uuid
import time
from urllib.parse import urlparse, parse_qs

def internalSolve(url):
    try:
        url = url.replace("lockr.so", "lockr.net")
        IDLE = str(uuid.uuid4())
        ID = url.replace("https://lockr.net/", "")
        
        rContent = parse_qs(urlparse(url).query).get('r', [None])[0]
        
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://lockr.net/"
        })
        
        session.get(url)
        
        session.get("https://clerk.lockr.net/v1/environment?__clerk_api_version=2025-11-10&_clerk_js_version=5.117.0") # retarded request
        session.get("https://clerk.lockr.net/v1/client?__clerk_api_version=2025-11-10&_clerk_js_version=5.117.0")# retarded request
        
        j = session.get(f"https://lockr.net/api/v1/lockers/{ID}/view").json()
        
        print(f"debug view response: {j}")
        
        if "BLOCKED_PROXY" in str(j):
            print("solving recaptcha... (u gotta handle captcha token yourself now niggga, i'm not giving free cc access)")
            
            # HDK = your_captcha_solver("recaptcha", "https://lockr.net", "6Lf_sZMrAAAAANq61XUHEAhAKt9Pxrb73JmmZzF1")
           
            # for now just error out, replace with real solver
            return "bypass fail! need captcha solver nigga", False
            
            # CAPRE = session.post("https://lockr.net/api/v1/captcha/verify", json={"token": HDK})
            # j = session.get(f"https://lockr.net/api/v1/lockers/{ID}/view").json()
            
            # `^^^ useless now
        
        try:
            token = j["data"]["token"]
        except:
            return "bypass fail! It appears that the lockr.net servers or bypass are down. Please try again later. (INVALID_API_RESPONSE)", False
        
        print(f"📎 LockrBY - Obtained session for {ID}-{IDLE}")
        
        time.sleep(60)  # they want u to wait
        
        for task in j.get("data", {}).get("tasks", []):
            w = session.get(f"https://lockr.net/api/v1/lockers/{ID}/task?token={token}")
            print(f"did a task {w.status_code}")
        
        unlock_url = f"https://lockr.net/api/v1/lockers/{ID}/unlock?token={token}"
        if rContent:
            unlock_url += f"&r={rContent}"
        
        r = session.get(unlock_url)
        print(f"unlock response: {r.text[:500]}...")
        
        target = r.json()["data"]["target"]
        print(f"Bypassed cockrso for link {IDLE}")
        
        try:
            session.close()
        except:
            pass
        return target, True
        
    except Exception as e:
        try:
            session.close()
        except:
            pass
        error_trace = traceback.format_exc()
        errorid = str(uuid.uuid4())
        print(f"Fatal Errror bypassing {url} - {errorid}")
        print(error_trace)
        return f"bypass fail! Fatal error bypassing your link, ErrorID : {errorid}", False

def getDest(url):
    for i in range(3):
        res, success = internalSolve(url)
        if success:
            return res, success
        print(f"retrying with {url[:50]}... ({res})")
        time.sleep(2)
    return res, False
    
    
print(getDest("https://lockr.net/5YRTnRwwd"))