# yolo-trainer

Шаблон проекта для подготовки датасетов и обучения YOLO-моделей с помощью `ultralytics`.

## ⚙️ Требования

- Python 3.10+;
- NVIDIA GPU и драйвер с поддержкой CUDA.

`requirements.txt` использует PyTorch wheels из индекса `https://download.pytorch.org/whl/cu130`. Если нужна другая версия CUDA, замените индекс на подходящий из PyTorch.

## 🛠️ Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/fibit/yolo-trainer
   cd yolo-trainer
   ```

2. Создайте виртуальное окружение:

   ```bash
   python -m venv .venv
   ```

3. Активируйте виртуальное окружение:

   ```bash
   .venv\Scripts\activate    # Windows
   source .venv/bin/activate # Linux
   ```

4. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

## 📁 Структура

```text
.
├── datasets/
│   └── <DatasetName>/
│       ├── data.yaml
│       ├── train/
│       │   ├── images/
│       │   └── labels/
│       ├── valid/
│       │   ├── images/
│       │   └── labels/
│       └── test/
│           ├── images/
│           └── labels/
├── runs/
├── dataset.py
├── requirements.txt
└── README.md
```

## 🧾 Формат датасета

Разметка должна быть в YOLO-формате:

```text
<class_id> <x_center> <y_center> <width> <height>
```

Координаты нормализованы в диапазоне `0..1`.

Пример `data.yaml`:

```yaml
train: train/images
val: valid/images
test: test/images

nc: 2
names: ['class_0', 'class_1']
```

`nc` должен совпадать с количеством классов в `names`.

## 🧱 Создание датасета

Создать пустую структуру датасета можно командой:

```bash
python dataset.py DatasetName
```

Скрипт создаст папки `train/`, `valid/`, `test/` с подпапками `images/` и `labels/`, а также файл `data.yaml`. Перед обучением заполните в `data.yaml` значения `nc` и `names`.

## 🚀 Обучение

Запустите обучение из корня проекта после активации виртуального окружения и установки зависимостей:

```bash
yolo task=detect mode=train model=yolo26n.pt data=./datasets/DatasetName/data.yaml epochs=100 imgsz=320 batch=32 degrees=180 scale=0.5 mosaic=1.0 flipud=0.5 fliplr=0.5 hsv_h=0.015 hsv_s=0.7 hsv_v=0.4 name=DatasetName
```

Замените `DatasetName` на имя папки датасета в `datasets/`, а `model=yolo26n.pt` - на нужную модель или путь к весам.

Основные параметры:

- `task=detect` - задача детекции объектов;
- `mode=train` - режим обучения;
- `model=yolo26n.pt` - стартовые веса модели;
- `data=.../data.yaml` - конфигурация датасета;
- `epochs=100` - количество эпох;
- `imgsz=320` - размер входного изображения;
- `batch=32` - размер batch;
- `degrees=180` - случайный поворот изображения;
- `scale=0.5` - случайное масштабирование;
- `mosaic=1.0` - вероятность mosaic-аугментации;
- `flipud=0.5` - вероятность вертикального отражения;
- `fliplr=0.5` - вероятность горизонтального отражения;
- `hsv_h=0.015` - изменение оттенка;
- `hsv_s=0.7` - изменение насыщенности;
- `hsv_v=0.4` - изменение яркости;
- `name=DatasetName` - имя запуска в `runs/detect/`.

## 📊 Результаты

После обучения артефакты сохраняются в:

```text
runs/detect/<name>/
```

Основные файлы:

- `weights/best.pt` - лучшие веса по метрике валидации;
- `weights/last.pt` - веса последней эпохи;
- `results.csv` - метрики по эпохам;
- `results.png` - графики обучения;
- `confusion_matrix.png` - матрица ошибок.

## 🧪 Валидация

```bash
yolo task=detect mode=val model=runs/detect/DatasetName/weights/best.pt data=./datasets/DatasetName/data.yaml imgsz=320
```

## 🎯 Предсказание

```bash
yolo task=detect mode=predict model=runs/detect/DatasetName/weights/best.pt source=./datasets/DatasetName/test/images imgsz=320
```
