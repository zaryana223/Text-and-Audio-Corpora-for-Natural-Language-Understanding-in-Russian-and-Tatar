# Ноутбук `zero_shot+few_shot_version.ipynb`

Оценка **генеративных LLM** на русском NLU без дообучения: модель получает промпт и возвращает JSON `{intent, slots}`. Тест — `ru.test.conll` (532 реплики после фильтрации интентов из списка `INTENTS`).

Результаты по моделям и сценариям собираются в `generative_error_analysis_tables.xlsx` (папка `data/errors/`).

---

## 1. Режимы эксперимента

| Режим | Флаг | Что подаётся модели | Зачем |
|--------|------|---------------------|--------|
| **Zero-shot** | `RUN_ZERO_SHOT = True` | Только `SYSTEM_PROMPT` + текст реплики | Базовая способность LLM без примеров |
| **Few-shot** | `RUN_FEWSHOT = True` | Промпт + 1–10 пар «запрос → JSON» из train + тестовая реплика | Проверка, помогают ли демонстрации из `ru.train.conll` |

Общие настройки в начале ноутбука:

| Параметр | Назначение |
|----------|------------|
| `ACTIVE_MODEL` | Какая модель грузится из `MODEL_REGISTRY` (например `Phi-4-mini-instruct`) |
| `DEFAULT_QUANT` | Квантизация: `4bit` или `fp16` |
| `SMOKE_N` | Если > 0 — взять только первые N реплик теста (быстрая проверка) |
| `SAVE_DIR` | Куда пишутся логи и метрики (Colab: Google Drive `nlu_results`) |

---

## 2. Модели (`MODEL_REGISTRY`)

| Ключ в ноутбуке | Hugging Face ID | Семейство чата |
|-----------------|-----------------|----------------|
| `Qwen2.5-3B-Instruct` | Qwen/Qwen2.5-3B-Instruct | qwen |
| `Qwen2.5-7B-Instruct` | Qwen/Qwen2.5-7B-Instruct | qwen |
| `google/gemma-2-2b-it` | google/gemma-2-2b-it | gemma |
| `google/gemma-2-9b-it` | google/gemma-2-9b-it | gemma |
| `Phi-4-mini-instruct` | microsoft/Phi-4-mini-instruct | qwen |
| `Mistral-7B-Instruct-v0.3` | mistralai/Mistral-7B-Instruct-v0.3 | qwen |

Для **Gemma** системный промпт вставляется в одно user-сообщение; для Qwen/Mistral/Phi — отдельные роли `system` и `user`.

---

## 3. Zero-shot: как устроен код

| Шаг | Функция / блок | Действие |
|-----|----------------|----------|
| 1 | `SYSTEM_PROMPT` | Список 16 интентов, слотов и правил (JSON на выходе, без выдуманных слотов) |
| 2 | `parse_conll_to_dicts` | Чтение `ru.test.conll` → текст, gold intent, gold slots, BIO |
| 3 | `load_model` | Загрузка LLM (4-bit через `bitsandbytes`, GPU) |
| 4 | `_build_messages_zeroshot(text)` | Сборка chat-сообщений без примеров |
| 5 | `_generate` → `_parse_output` | `model.generate` → разбор JSON intent/slots |
| 6 | `generate_prediction_zeroshot(text)` | Обёртка для одной реплики |
| 7 | `run_evaluation(..., "zero_shot")` | Прогон по всему тесту + метрики |

**Запуск одного эксперимента:**

```python
run_evaluation(generate_prediction_zeroshot, "zero_shot", model_name=MODEL_NAME)
```

---

## 4. Few-shot: как устроен код

| Шаг | Функция / блок | Действие |
|-----|----------------|----------|
| 1 | `FEWSHOT_CONFIGS` | Набор интентов, для которых нужны примеры |
| 2 | `get_fewshot_examples(intents)` | По каждому интенту — одна «богатая» реплика из `ru.train.conll` (много слотов) |
| 3 | `_build_messages_fewshot(text, examples)` | В историю чата: user → assistant (JSON) для каждого примера, затем тест |
| 4 | `generate_prediction_fewshot(text, examples)` | Генерация с подсказками |
| 5 | `run_evaluation(lambda t, ex=examples: generate_prediction_fewshot(t, ex), exp_type, fewshot_examples=examples)` | Отдельная папка результатов на конфигурацию |

### Конфигурации few-shot

| ID эксперимента (`exp_type`) | Интенты в примерах | Смысл |
|------------------------------|-------------------|--------|
| `few_shot_1_popular` | `weather/find` | 1 пример — самый частый интент |
| `few_shot_1_problem` | `SearchScreeningEvent` | 1 пример — интент с частыми ошибками |
| `few_shot_1_slots` | `BookRestaurant` | 1 пример — много слотов |
| `few_shot_5` | 5 интентов (погода, ресторан, кино, будильник, напоминание) | Короткий набор |
| `few_shot_10` | 10 разных интентов | Расширенный набор |

Имя папки на диске: `{SAVE_DIR}/{exp_type}/{MODEL_NAME}/`.

---

## 5. Сравнение zero-shot и few-shot

| | Zero-shot | Few-shot |
|---|-----------|----------|
| Примеры в промпте | Нет | 1–10 реплик из train |
| Папка результатов | `zero_shot/<модель>/` | `few_shot_* /<модель>/` |
| Доп. файл | — | `fewshot_examples.json` (какие примеры использовались) |
| Ожидаемый эффект в ВКР | Базовый уровень | Небольшой прирост по интентам; слоты всё равно слабее энкодеров |

---

## 6. Метрики (`run_evaluation`)

| Метрика | Уровень | Описание |
|---------|---------|----------|
| Intent Accuracy | реплика | Доля верных интентов |
| Intent F1 macro / weighted | реплика | sklearn `f1_score` по классам |
| Slot Precision / Recall / F1 | span (тип + значение) | Совпадение множеств спанов в тексте |
| Slot F1 (seqeval) | BIO-последовательность | Span F1 по токенам (как у энкодеров) |
| Joint (в сводках ВКР) | — | Обычно `(Intent F1 weighted + Span F1) / 2` из `metrics_summary.json` |

Дополнительно помечаются «слабые» интенты/слоты (редкие в train, порог 500 вхождений).

---

## 7. Выходные файлы (на один прогон)

| Файл | Содержание |
|------|------------|
| `metrics_summary.json` | Сводные метрики эксперимента |
| `results.csv` | По каждой реплике: текст, gold/pred intent, слоты, confidence |
| `log.txt` | Подробный лог |
| `per_slot_bio.csv` | F1 по типам слотов (seqeval) |
| `per_slot_span.csv` | F1 по типам слотов (строгое совпадение span) |
| `fewshot_examples.json` | Только для few-shot: тексты примеров |
| `checkpoint.json` | Промежуточное сохранение каждые 10 реплик (можно продолжить) |

Сводка по всем экспериментам модели: `summary_<MODEL_NAME>.csv` в `SAVE_DIR`.

---

## 8. Зависимости и окружение

`transformers`, `accelerate`, `bitsandbytes`, `torch`, `pandas`, `seqeval`, `scikit-learn`, `tqdm`. Рекомендуется GPU (в ноутбуке — Colab L4). Для gated-моделей — токен Hugging Face (`HF_TOKEN`).

---

## Связь с репозиторием

| Артефакт | Где |
|----------|-----|
| Код экспериментов | [zero_shot+few_shot_version.ipynb](../zero_shot+few_shot_version.ipynb) |
| Таблицы ошибок LLM | [data/errors/generative_error_analysis_tables.xlsx](../data/errors/generative_error_analysis_tables.xlsx) |
| Метрики энкодеров / GigaAM | [nlu_metrics/](../nlu_metrics/), [run_metrics.py](../run_metrics.py) |
