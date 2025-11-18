# -*- coding: utf-8 -*- 
from lxml import html
import requests
import random
import string
import json
import uuid
import time
import re
import os
import threading 
import sys # Slow-print এবং stdout ব্যবহারের জন্য এটি যোগ করা হয়েছে

# --- কালার কোড (For beautiful output) ---
# যদিও ব্যানারে সরাসরি ANSI কোড ব্যবহার করা হয়েছে, অন্যান্য প্রিন্ট স্টেটমেন্টের জন্য এগুলো রাখা হলো।
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
MAGENTA = '\033[95m' 
ENDC = '\033[0m' # Reset color

# --- AMNAH ব্যানার ফাংশন (বৃহৎ, রঙিন ও স্লো-প্রিন্ট ইফেক্ট) ---
def print_banner():
    # ক্লিয়ার স্ক্রিন
    os.system('cls' if os.name == 'nt' else 'clear') 
    
    # ব্যবহারকারীর দেওয়া ব্যানার কোড, সরাসরি ANSI কালার কোড সহ
    ban = f'''
\033[0;92m╔══════════════════════════════════════════════╗
\033[0;92m║███████ \033[0;31m██    ██ \033[0;93m██████  \033[0;32m█████\033[0;31m███  ██████\033[0;92m     ║  
\033[0;92m║██      \033[0;31m██    ██ \033[0;93m██   ██    \033[0;32m██    \033[0;31m██    ██\033[0;92m    ║ 
\033[0;92m║███████ \033[0;31m██    ██ \033[0;93m██████     \033[0;32m██    \033[0;31m██    ██\033[0;92m    ║ 
\033[0;92m║     ██ \033[0;31m██    ██ \033[0;93m██         \033[0;32m██    \033[0;31m██    ██\033[0;92m    ║ 
\033[0;92m║███████  \033[0;31m██████  \033[0;93m██         \033[0;32m██     \033[0;31m██████\033[0;92m     ║  
\033[0;92m╚══════════════════════════════════════════════╝
\033[0;92m╔═══════════════════════════════════════════╗\033[0;92m╔═══╗
\033[0;92m║➣\033[0;31m DEVOLPER   :   \033[0;34m       FJ RIYAD           ║\033[0;32m║\033[1;31m S \033[1;32m║
\033[0;92m║➣\033[0;33m FACEBOOK   :    \033[0;35m      সুপ্ত প্রতিভা         ║\033[0;32m║\033[1;312m U\033[0;92m ║
\033[0;92m║═══════════════════════════════════════════║\033[0;32m║\033[1;34m P\033[0;92m ║
\033[0;92m║➣\033[0;91m WHATSAPP   :    \033[0;92m      01309933049        ║\033[0;32m║\033[1;93m T\033[0;92m ║
\033[0;92m║➣\033[0;93m GITHUB     :     \033[0;94m    premium-All-Command ║\033[0;92m║\033[1;92m O\033[0;92m ║
\033[0;92m║➣\033[0;94m TOOLS      :      \033[0;93m    FACEBOOK FOLLOW       ║\033[0;92m║ 😘║
\033[0;92m╚═══════════════════════════════════════════╝\033[0;92m╚═══╝
'''
    # স্লো-প্রিন্ট ইফেক্ট
    for h in ban:
        sys.stdout.write(h)
        sys.stdout.flush()
        time.sleep(0.0025)

# --- ১. ফাইল থেকে কুকি লোড করা ---
def load_cookies_from_file(file_path):
    """Loads cookies from a file, one per line."""
    try:
        with open(file_path, 'r') as f:
            cookies = [line.strip() for line in f if line.strip()]
        return cookies
    except FileNotFoundError:
        print(f"{RED}[ERROR] The file '{file_path}' was not found.{ENDC}")
        return []
    except Exception as e:
        print(f"{RED}[ERROR] An error occurred while reading the file: {e}{ENDC}")
        return []

# --- ২. কুকি ইনপুট অপশন ---
def get_cookies():
    print(f"\n{BLUE}--- Cookie Input Options ---{ENDC}")
    print(f"1) {YELLOW}Manual Cookie Input{ENDC} (Single or multiple, separated by comma)")
    print(f"2) {YELLOW}Upload from cookies.txt File{ENDC} (One cookie per line)")
    
    choice = input(f"Enter your choice (1 or 2): ")
    
    if choice == '1':
        # ম্যানুয়াল ইনপুট
        cookies_input = input("Enter cookies (separate with comma): ")
        cookie_list = [c.strip() for c in cookies_input.split(',') if c.strip()]
        return cookie_list
    elif choice == '2':
        # ফাইল ইনপুট
        file_path = input("Enter the path to the cookies file (e.g., /sdcard/cookies.txt): ")
        return load_cookies_from_file(file_path)
    else:
        print(f"{RED}Invalid choice. Exiting.{ENDC}")
        return []

# --- ৪. পুরো প্রসেসিং লজিককে একটি ফাংশনের মধ্যে নেওয়া হয়েছে ---
def process_cookie(i, cookie_main, url, react_id, page_limit, sleep_delay, total_cookies):
    # --- Feedback ID বের করা ---
    headers = {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': cookie_main, 
        'dpr': '1',
        'pragma': 'no-cache',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.71", "Google Chrome";v="120.0.6099.71"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"6.5.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'viewport-width': '814',
    }

    params = {
        'app': 'fbl',
    }

    feedback_id = None
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10) 
        response.raise_for_status()
        
        match = re.search(r'"feedback":{"id":"(.*?)"', response.text)
        if match:
            feedback_id = match.group(1)
            print(f"  {GREEN}[INFO] Cookie {i + 1}/{total_cookies} - Feedback ID: {feedback_id}{ENDC}")
        else:
            print(f"  {RED}[ERROR] Cookie {i + 1}/{total_cookies} - Feedback ID not found. Cookie might be invalid or expired.{ENDC}")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"  {RED}[ERROR] Cookie {i + 1}/{total_cookies} - Failed to get post data/network error: {e}. Skipping.{ENDC}")
        return 

    # --- Access Token বের করা ---
    headers = {
        'Host': 'business.facebook.com',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cookie': cookie_main, 
    }

    TOKEN = None
    try:
        response = requests.get('https://business.facebook.com/content_management', headers=headers, timeout=10)
        response.raise_for_status()
        
        match = re.search(r'"accessToken":"(EAA.*?)","', response.text)
        if match:
             TOKEN = match.group(1)
             print(f"  {GREEN}[INFO] Cookie {i + 1}/{total_cookies} - Access Token found.{ENDC}")
        else:
             print(f"  {RED}[ERROR] Cookie {i + 1}/{total_cookies} - Token not found in business page. Skipping.{ENDC}")
             return 
             
    except requests.exceptions.RequestException as e:
        print(f"  {RED}[ERROR] Cookie {i + 1}/{total_cookies} - Failed to get token/network error: {e}. Skipping.{ENDC}")
        return 
        
    # --- Page ID গুলো বের করা ---
    headers = {'cookie': cookie_main} 

    params = {
        'access_token': TOKEN,
        'fields': 'accounts{additional_profile_id}'
    }

    page_ids = []
    try:
        response = requests.get('https://graph.facebook.com/v19.0/me', params=params, headers=headers, timeout=10)
        response.raise_for_status()
        response_json = response.json()
        
        if 'accounts' in response_json and 'data' in response_json['accounts']:
            for node in response_json['accounts']['data']:
                if len(page_ids) == page_limit:
                    break
                if 'additional_profile_id' in node:
                     page_ids.append(node['additional_profile_id'])
        print(f"  {YELLOW}[STATUS] Cookie {i + 1}/{total_cookies} - Loaded {len(page_ids)} pages for reaction.{ENDC}")
        
    except requests.exceptions.RequestException as e:
        print(f"  {RED}[ERROR] Cookie {i + 1}/{total_cookies} - Failed to get page IDs/network error: {e}. Skipping.{ENDC}")
        return
    except Exception as e:
        print(f"  {RED}[ERROR] Cookie {i + 1}/{total_cookies} - An unexpected error occurred while getting Page IDs: {e}{ENDC}")
        return


    # --- Reaction দেওয়া শুরু ---
    for j, page_id in enumerate(page_ids):
        actor_id = page_id

        cookie_with_actor = cookie_main + f';i_user={actor_id};' 

        dtsg, lsd = get_dtsg_ls(cookie_with_actor)

        headers = {
            'Host': 'www.facebook.com',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Viewport-Width': '1920',
            'X-Fb-Friendly-Name': 'CometUFIFeedbackReactMutation',
            'X-Fb-Lsd': lsd,
            'Sec-Ch-Ua-Platform-Version': '"6.5.0"',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Asbd-Id': '129477',
            'Dpr': '1',
            'Sec-Ch-Ua-Full-Version-List': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.71", "Google Chrome";v="120.0.6099.71"',
            'Sec-Ch-Ua-Model': '""',
            'Sec-Ch-Prefers-Color-Scheme': 'dark',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Accept': '*/*',
            'Origin': 'https://www.facebook.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': url,
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cookie': cookie_with_actor, 
        }

        data = {
            'av': actor_id,
            '__aaid': '0',
            '__user': actor_id,
            '__a': '1',
            '__req': 'o',
            '__hs': '19825.HYP:comet_pkg.2.1..2.1',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1012737330',
            '__s': 'rhiy7q:qkk91d:6py9mw',
            '__hsi': '7357019383365289808',
            '__dyn': '7AzHK4HwBgDx-5Q1ryaxG4Qih09y2O5U4e2C3-ubyQdwSAx-bwNw9G2Saxa1NwJwpUe8hw8u2a0Z82_CxS320om78c87m2210wEwgo9oO0wE7u12wOx62G5Usw9m1cwLwBgK7o8417wc61awko5m1mzXw8W58jwGzEjxq1jxS6FobrwKxm5oe8cEW4-5pUfEe88o4qum7-2K0-poarCwLyES1Iwh888cA0z8c84q58jyUaUcojxK2B08-269wkopg6C13whEeEfE-VU-4Edouwm8',
            '__csr': 'gbQj6PihcgJnfPhJq2itv9qqOZtN4AZn8TahSBGSDteGjl5PQBXblnmBIAWWlsyGAGaDDQAlaAQnF5WVVWGVtpFHDijWyumHS8GVyBUNkbzpKGGiESKvVSmarDBBKV4XAWhaAiDx255BxijWzKiQ8AKU8pWDACUzz8iK8AzFqDDyUKbWyu58-4EOWl2VE-q48kgK8yGxu2a9CxaA7ooyUiwxgN1HBBxHwGK9xry8hh-2aummqeyEuwHU-m2m4oCK48jx128lyokCgS5Ue8y9xScxG2-5oW4ojwKyUug9bUsxai5EpwDy84K5ohG7oa8abzFpUe8W1-x2uq1SxG7EhBxe6Ub8vwvo1VE1iEtgKcvU3rwsobEogpxerw24U8o6q0hu0hS5EjwXBx6Q8gpyU8Ugw3Ko12qwywCw6Lw0wmw1qZ06ByE0Ku2G0SUfoeU10U045S03yC02u0V3G2t0Gx100E0wAw13i0XohVqwb6qA3t048g1a81pU3dwOg5S09_w-w48w18e0lG0ja1Hxi053Exws8F4xeE1UE1jU1bS09jwFwv8189BQ5Q0I11z2pSbGon44fHi2Vohe620hVmA0j2fwsHiS0bow5mwOCxC2p00EEwaS2O5vda0btxcTo3Zo09zUc85y19Tw77pox03Y44o38wPw2gEao0Npw',
            '__comet_req': '15',
            'fb_dtsg': dtsg,
            'jazoest': '25561',
            'lsd': lsd,
            '__spin_r': '1012737330',
            '__spin_b': 'trunk',
            '__spin_t': '1712939558',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
            'variables': '{"input":{"attribution_id_v2":"CometSinglePostRoot.react,comet.post.single,via_cold_start,1712939562435,981658,,,","feedback_id":"' + feedback_id + '","feedback_reaction_id":"' + react_id + '","feedback_source":"OBJECT","session_id":"' + str(
                uuid.uuid4()) + '","actor_id":"' + actor_id + '","client_mutation_id":"1"},"useDefaultActor":false,"scale":1}',
            'server_timestamps': 'true',
            'doc_id': '6880473321999695',
        }

        try:
             response = requests.post('https://www.facebook.com/api/graphql/', headers=headers, data=data, timeout=10)
             
             if response.status_code == 200 and '"errors"' not in response.text:
                 print(f"    {GREEN}[SUCCESS] Page ID {actor_id} ({j+1}/{len(page_ids)}): Reaction successful.{ENDC}")
             else:
                 print(f"    {RED}[FAILURE] Page ID {actor_id} ({j+1}/{len(page_ids)}): Failed. Status: {response.status_code}.{ENDC}")
        except requests.exceptions.RequestException as e:
            print(f"    {RED}[NETWORK ERROR] Failed to send reaction for {actor_id}: {e}{ENDC}")

        # --- রিয়্যাকশন ডিলে (Delay) ---
        time.sleep(sleep_delay) 
    
    print(f"{BLUE}--- Finished processing Cookie {i + 1}. Moving to the next one... ---{ENDC}")
    time.sleep(5)


# ... (get_rand ফাংশন অপরিবর্তিত) ...
def get_rand(
        length: int,
        c_letter: bool = True,
        s_letter: bool = True,
        numbers: bool = True,
        symbols: bool = False,
):
    text = ""
    if c_letter:
        text += string.ascii_uppercase
    if s_letter:
        text += string.ascii_lowercase
    if numbers:
        text += string.digits
    if symbols:
        text += string.punctuation

    return "".join(random.choice(text) for _ in range(length))


# ... (get_dtsg_ls ফাংশন অপরিবর্তিত) ...
def get_dtsg_ls(cookie_):
    headers_ = {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': cookie_,
        'dpr': '1.1',
        'pragma': 'no-cache',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="119.0.6045.159", "Chromium";v="119.0.6045.159", "Not?A_Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"6.3.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS armv7l 4537.56.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'viewport-width': '1073',
    }

    try:
        resp_ = requests.get('https://www.facebook.com', headers=headers_, timeout=10)
        resp_.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return get_rand(22), get_rand(22)

    soup_ = html.fromstring(resp_.content)
    tree_ = soup_
    
    try:
        lsd_text_ = tree_.xpath('//script[not(@nonce) and contains(text(), "LSD") and contains(text(), "token")]/text()')[0]
        exp_ = re.compile('"LSD".*token')
        lsd_start_ = exp_.search(lsd_text_).group().find("{")
        lsd_end_ = exp_.search(lsd_text_).group().find("}")
        lsd_ = json.loads(exp_.search(lsd_text_).group()[lsd_start_: lsd_end_ + 1])["token"]
    except:
        lsd_ = get_rand(22) 

    try:
        val_ = soup_.xpath('//script[@id="__eqmc"]/text()')[0]
        obj_ = json.loads(val_)
        fb_dtsg_ = obj_["f"]
    except Exception as e:
        fb_dtsg_ = get_rand(22) 
    
    return fb_dtsg_, lsd_


# --- মেইন প্রোগ্রাম শুরু ---
print_banner() 

cookie_list = get_cookies()

if not cookie_list:
    print(f"{RED}No cookies were loaded. Exiting.{ENDC}")
    exit()

print(f"{BLUE}--- Configuration ---{ENDC}")
url = input(f"Enter the post URL: ")

# --- রিয়্যাকশন স্পিড কন্ট্রোল ---
default_delay = 0.1 
try:
    delay_input = input(f"Enter delay between reactions in seconds (Recommended: 0.1 for max speed. Press Enter for {default_delay}s): ")
    sleep_delay = float(delay_input) if delay_input else default_delay
except ValueError:
    print(f"{YELLOW}Invalid delay value. Using default: {default_delay}s.{ENDC}")
    sleep_delay = default_delay

print(f"Selected reaction delay: {GREEN}{sleep_delay} seconds{ENDC}")

# --- থ্রেডিং ইনপুট ---
thread_choice = input(f"\n{YELLOW}Do you want to use threading for faster processing? (y/n): {ENDC}").lower()
use_threading = thread_choice == 'y'

print(f"\n{BLUE}--- Reaction Type ---{ENDC}") 
print(f"1 = love, 2 = haha, 3 = wow, 4 = sad, 5 = angry, 6 = care, 7 = like")
react = int(input("Enter the reaction: "))

page_limit = 15

# --- Reaction ID সেট করা (Cython-সামঞ্জস্যপূর্ণ) ---
react_id = None
if react == 1:
    react_id = "1678524932434102" # love
elif react == 2:
    react_id = "115940658764963" # haha
elif react == 3:
    react_id = "478547315650144" # wow
elif react == 4:
    react_id = "908563459236466" # sad
elif react == 5:
    react_id = "444813342392137" # angry
elif react == 6:
    react_id = "613557422527858" # care
elif react == 7:
    react_id = "1635855486666999" # like

if react_id is None:
    print(f"{RED}Invalid reaction choice. Exiting.{ENDC}")
    exit()

threads = []
total_cookies = len(cookie_list)

# --- ৩. প্রতিটা কুকির ওপর লুপ (থ্রেডিং লজিক) ---
for i, cookie_main in enumerate(cookie_list):
    print(f"\n{BLUE}--- Starting process for Cookie {i + 1}/{total_cookies} ---{ENDC}")

    if use_threading:
        # থ্রেডিং চালু থাকলে, প্রতিটি কুকিকে আলাদা থ্রেডে পাঠানো হবে
        t = threading.Thread(target=process_cookie, args=(i, cookie_main, url, react_id, page_limit, sleep_delay, total_cookies))
        threads.append(t)
        t.start()
        # এখানে কোনো delay নেই, কারণ থ্রেডগুলো একসাথে চলবে
    else:
        # থ্রেডিং বন্ধ থাকলে, সিকোয়েন্সিয়ালি কাজ হবে
        process_cookie(i, cookie_main, url, react_id, page_limit, sleep_delay, total_cookies)
        # প্রতিটি কুকি প্রসেস করার পর একটি ছোট বিরতি
        time.sleep(5)


# থ্রেডিং চালু থাকলে, সব থ্রেড শেষ না হওয়া পর্যন্ত অপেক্ষা করুন
if use_threading:
    for t in threads:
        t.join()
    print(f"\n{GREEN}All processes finished!{ENDC}")
