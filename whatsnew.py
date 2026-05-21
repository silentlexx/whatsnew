#!/usr/bin/python3
from bs4 import BeautifulSoup as bs  # type: ignore
import requests as req
import subprocess as sub
from packaging import version
from selenium import webdriver # type: ignore
from selenium.webdriver.firefox.service import Service # type: ignore
from selenium.webdriver.firefox.options import Options # type: ignore



kernel_url = "https://www.kernel.org/"
nvidia_url = "https://www.nvidia.com/en-us/drivers/unix/"
nv_run = f"CC=clang LD=ld.lld HOSTCC=clang HOSTLD=ld.lld IGNORE_CC_MISMATCH=1 /home/silentlexx/src/NVIDIA_Latest.run"

GECKODRIVER_PATH = '/home/silentlexx/src/geckodriver' 

def parse_site(site):
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Виконання в headless режимі, без відкриття браузера
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.set_preference('intl.accept_languages', 'uk-UA')
    # Створення сервісу для geckodriver
    webdriver_service = Service(GECKODRIVER_PATH)
    # Створення WebDriver
    driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)
    driver.get(site)
    # Отримання HTML-коду сторінки
    html = driver.page_source
    # Парсинг HTML-коду за допомогою BeautifulSoup
    soup = bs(html, 'html.parser')
    driver.quit()
    #sub.Popen(["killall", "firefox-esr"], )
    return soup


def get_kernel_ver():
    out = sub.run(["uname", "-r"], text=True, capture_output=True)
    return out.stdout.strip().split("-")[0]

def get_nvidia_ver():
    out = sub.run(["nvidia-settings", "-v"], text=True, capture_output=True)
    return out.stdout.splitlines()[1].split(":")[1].replace("version", "").strip()

def get_newest_kernel_ver():
    res = req.get(kernel_url)
    if req:
        s = bs(res.content, 'html.parser')
        return s.select_one("#latest_link a").text.strip()
    return "unknown"

def get_newest_nvidia_ver():
    s = parse_site(nvidia_url)
    if not s:
        return "unknown", "unknown"

    latest_prod_text = s.find(string="Latest Production Branch Version:")
    latest_prod = latest_prod_text.find_next('a') if latest_prod_text else None

    latest_beta_text = s.find(string="Latest Beta Version:")
    latest_beta = latest_beta_text.find_next('a') if latest_beta_text else None

    latest_nfb_text = s.find(string="Latest New Feature Branch Version:")
    latest_nfb = latest_nfb_text.find_next('a') if latest_nfb_text else None

    versions = []
    if latest_prod:
        versions.append((latest_prod.text.strip(), latest_prod['href']))
    if latest_beta:
        versions.append((latest_beta.text.strip(), latest_beta['href']))
    if latest_nfb:
        versions.append((latest_nfb.text.strip(), latest_nfb['href']))

    if versions:
        highest_version = max(versions, key=lambda x: version.parse(x[0]))
        return highest_version

    return "unknown", "unknown"

def reboot():
    ans = input("Reboot system now [y/N]?: ")
    if ans.casefold() == "y": 
        sub.run(["sudo", "reboot"], text=True)


def dwn_nv(url):
    s = parse_site(url)

    if s:
        a = s.select_one(".nv-driver-button-standard a.btn-content")
        
        if a:
            file = a['href']
            sub.run(["rm", nv_run], text=False)
            sub.run(["wget", "-O", nv_run, file], text=True)
            sub.run(["chmod", "+x", nv_run], text=False)
            sub.run(["sudo", nv_run, "--accept-license","--no-rpms", "--no-recursion", "--dkms", "--install-libglvnd", "--force-libglx-indirect", "--no-check-for-alternate-installs", "--no-precompiled-interface", "--no-x-check", "--allow-installation-with-running-driver","--rebuild-initramfs", "--systemd" ], text=True )
            reboot()

def main():
    sk = get_kernel_ver()
    sn = get_nvidia_ver()

    print("System:")
    print(f"Kernel {sk}\nNVIDIA {sn}\n")

    nk = get_newest_kernel_ver()
    nn, dwn = get_newest_nvidia_ver()

    print("Newest:")
    print(f"Kernel {nk}\nNVIDIA {nn}\n")

    if version.parse(nk) > version.parse(sk):
        ans = input(f"Run update-tkg to update kernel {nk} [y/N]?: ")
        if ans.casefold() == "y":
            sub.run(["update-tkg"], text=True)
            reboot()

    if version.parse(nn) > version.parse(sn) and nn != "unknown":
        ans = input(f"Download new NVIDIA drivers {nn} [y/N]?: ")
        if ans.casefold() == "y":
            dwn_nv(dwn)
       
if __name__=="__main__":
    main()