# django_yandex_intensive

# Быстрый запуск

#### 1. Клонирование репозитория
```git clone https://github.com/JeeEssEm/django_yandex_intensive```  
```cd django_yandex_intensive```
#### 2. Создание виртуальной среды
```python -m venv venv```

#### 3. Активация виртуальной среды
> **Примечание:** в данном примере среда активируется в ОС Windows, Powershell.  
> Решение для **Unix или MacOS**, используя **bash**:  
> ```source venv/bin/activate```

```.\venv\Scripts\Activate.ps1```

#### 4. Установка зависимостей
> **Примечание:** в проекте есть несколько файлов для установки зависимостей:  
> ```requirements.txt``` — основные зависимости  
> ```requirements_for_dev.txt``` — зависимости для разработки  
> ```requirements_for_testing.txt``` — зависимости для тестирования  

```pip install -r requirements.txt```

#### 5. Переменные окружения (.env)
Создайте ".env" файл в корне проекта и добавьте в него переменную
SECRET_KEY с значением секретного ключа и переменную DEBUG со значением True
или False для запуска проекта в режиме отладки.  
Переменная ALLOWED_HOSTS принимает хосты, перечисленные через запятую.
Пример:
```
ALLOWED_HOSTS=127.0.0.1,localhost
```

#### 6. Запуск проекта
```python manage.py runserver```

