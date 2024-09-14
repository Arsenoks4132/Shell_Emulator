# Запуск эмулятора

Для запуска эмулятора необходимо выполнить следующую команду

```bash
py [path]/main.py [config]
```

Где:

- **path** -- Путь до директории с эмулятором,
- **config** -- Конфигурационный файл, содержащий путь к архиву виртуальной файловой системы

# Команды эмулятора

## ls (list)

```bash
ls [directory]
```

Просмотр содержимого директории **directory**. При отсутствующем параметре **directory** выводится содержимое текущей директории.

### Тесты:

![image](https://github.com/user-attachments/assets/592e57f8-30af-4dc8-8f1a-47f5eff6e03a)

## cd (change directory)

```bash
cd [directory]
```

Изменение текущей директории на **directory**. При отсутствующем параметре **directory** директория изменяется на корневую.

### Тесты:

![image](https://github.com/user-attachments/assets/003e0991-588d-4efb-90eb-7480dd4efe6a)

## exit

Выход из эмулятора.

### Тесты:

![image](https://github.com/user-attachments/assets/528b7193-9842-460f-b341-93ee711b9902)

## touch

```bash
touch [file]
```

Создание файла с названием **file**.

### Тесты:

![image](https://github.com/user-attachments/assets/4d81129c-45c4-429d-94e7-2dec91567a62)

## head

```bash
head (-n <count>) [file]
```

Вывод первых **count** строчек из **file**. При отсутствующем флаге **-n** выводится первые 10 строчек файла.

### Тесты:

