#!/bin/bash

current_kernel=$(uname -r | sed -E 's/^([0-9]+\.[0-9]+\.[0-9]+).*/\1/')

# Отримуємо список встановлених пакетів з ядром *-tkg-bore
installed_kernels=$(dpkg --list | awk '{print $2}' | grep -E 'linux-.*-tkg-*')

# Формуємо список для видалення
remove_list=""
for kernel in $installed_kernels; do
    if [[ $kernel != *"$current_kernel"* ]]; then
        remove_list="$remove_list $kernel"
    fi
done

# Видаляємо знайдені старі ядра
if [[ -n "$remove_list" ]]; then
    echo "Видаляємо старі ядра: $remove_list"
    sudo apt remove --purge $remove_list
    sudo apt autoremove -y
else
    echo "Старих ядер для видалення немає."
fi


echo "Отримуємо список папок у /lib/modules/..."
kernel_dirs=$(ls -1 /lib/modules/)

for dir in $kernel_dirs; do
    if [[ $dir != "$current_kernel-tkg-bore" ]] && ! dpkg -l | grep -q "$dir"; then
        echo "Видаляємо зайву папку: /lib/modules/$dir"
        sudo rm -rf "/lib/modules/$dir"
    fi
done

echo "Очищення завершено!"