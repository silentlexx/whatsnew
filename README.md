# 🚀 kernel-nvidia-updater

Автоматизований Python-скрипт для моніторингу та оновлення ядра Linux (через `update-tkg`) та драйверів NVIDIA безпосередньо з офіційних джерел.

---

## 🔥 Основні можливості

* **Kernel Check:** Порівнює поточну версію з останнім релізом на [kernel.org](https://www.kernel.org/). Пропонує оновлення через `update-tkg`.
* **Smart NVIDIA Parsing:** Використовує *Selenium (headless Firefox)* для аналізу UNIX-гілок NVIDIA. Знаходить найвищу версію серед *Production, New Feature та Beta*.
* **Auto-Install:** Самостійно стягує `.run` інсталятор, чистить старі файли та запускає встановлення з оптимізованими прапорцями (`clang`/`lld`, DKMS, systemd, initramfs).
* **Interactive:** Безпечні запити підтвердження (`y/N`) перед кожною важливою дією.

## 🛠️ Залежності

```bash
pip install beautifulsoup4 requests selenium packaging
```
* **Система:** geckodriver, clang, ld.lld, wget, nvidia-settings.
* **Кастомізація:** Шляхи та прапорці збірки (IGNORE_CC_MISMATCH тощо) редагуються на початку скрипту.

## 📋 Запуск
```bash
python3 whatsnew.py
```
