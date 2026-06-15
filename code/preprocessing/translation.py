import openai
from dotenv import load_dotenv
import os
import time
import random

def log(msg):
    with open("run.log", "a", encoding="utf-8") as f:
        f.write(msg + "\n")


load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if api_key is None:
    log("ERROR: DeepSeek API key not found in .env")
    raise RuntimeError("DeepSeek API key missing")

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

log("DeepSeek client initialized")

def get_full_prompt(block):
    rules = """Правила перевода::

Русская разметка

1. Местоимение my переводим:

* переводи все/текущий в будильниках и напоминаниях

* либо переводим мой

1. Если в сущености встретилось тире, размечай как одну сущность

    1. Пример:

            1. 8 Татра B-location

            2. 9 - I-location

            3. 10 Национальном I-location

2. Если встречаются названия плейлистов, фильмов и т.п, то:

* либо оставляем оригинал

* либо если это популярное название, имя автора и т.п (как Гарри Поттер, Теория Большого Взрыва, Друзья и т.д), то адаптируем на русский.

1. Если встречаем в примерах AK (пример, Will it be colder four months from now in Suwanee AK ) — то оставляем его в оригинально виде.

2. В случае когда у нас время present continuous, то:

    * либо переводим как продолженное (пример,  Is The Two Gladiators playing - Играет Two Gladiators), т.е подразумевается процесс в данный промежуток времени.

    * либо если присутствует грамматический показатель будущ. времени, то переводим как будущее время. (пример, Is Any Which Way You Can playing in 15 seconds - Заиграет ли Any Which Way You Can через 15 секунд)

3. Если встречаем лгбт тематику в названиях и т.п, то меняем данный пример на разрешенный.


Пример английский

# text: Add a reminder for today at 4pm
# intent: reminder/set_reminder
1 Add O
2 a O
3 reminder O
4 for O
5 today B-datetime
6 at I-datetime
7 4pm I-datetime

Русский перевод

# text: добавь напоминание на сегодня на 4 часа дня
# intent: reminder/set_reminder
1 добавь O
2 напоминание O
3 на O
4 сегодня B-datetime
5 на I-datetime
6 4 I-datetime
7 часа I-datetime
8 дня I-datetime
"""
    instruction = f"\nПереведи этот текст на русский\n{block}\nОтвет:"
    return rules + instruction

def test_run(input_path, output_path, start_id=None, limit=None):
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except UnicodeDecodeError:
        with open(input_path, "r", encoding="cp1251") as f:
            content = f.read().strip()

    blocks = content.split("\n\n")
    log(f"Loaded {len(blocks)} blocks")

    start_idx = 0
    if start_id is not None:
        for i, block in enumerate(blocks):
            lines = block.splitlines()
            if lines and lines[0].strip() == start_id:
                start_idx = i
                break
        log(f"Starting from block index {start_idx} (id: {start_id})")

    selected_blocks = blocks[start_idx:]
    if limit is not None:
        selected_blocks = selected_blocks[:limit]

    log(f"Running on {len(selected_blocks)} samples")

    last_request_time = None

    with open(output_path, "a", encoding="utf-8") as out_f:
        for i, block in enumerate(selected_blocks):
            if not block.strip():
                continue

            lines = block.splitlines()
            block_id = lines[0] if lines else f"block_{i}"
            log(f"Processing {block_id}")

            full_prompt = get_full_prompt(block)

            if last_request_time is not None:
                elapsed = time.time() - last_request_time
                if elapsed < 2:
                    sleep_time = random.uniform(4, 6)
                else:
                    sleep_time = random.uniform(1, 3)
                log(f"Sleeping {sleep_time:.1f}s (last request took {elapsed:.1f}s)")
                time.sleep(sleep_time)

            MAX_RETRIES = 3
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    last_request_time = time.time()
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a professional translator and NLP specialist. Output ONLY CoNLL format."
                            },
                            {
                                "role": "user",
                                "content": full_prompt
                            }
                        ],
                        temperature=0,
                        timeout=30  
                    )
                    last_request_time = time.time()

                    translated_data = response.choices[0].message.content.strip()
                    out_f.write(translated_data + "\n\n")
                    out_f.flush()

                    log(f"SUCCESS {block_id}")
                    break  

                except Exception as e:
                    log(f"API ERROR {block_id} (attempt {attempt}/{MAX_RETRIES}): {repr(e)}")
                    if attempt < MAX_RETRIES:
                        retry_sleep = random.uniform(5, 10)
                        log(f"Retrying in {retry_sleep:.1f}s...")
                        time.sleep(retry_sleep)
                    else:
                        log(f"FAILED {block_id} after {MAX_RETRIES} attempts, skipping")

    log(f"Finished. Results saved to {output_path}")

test_run(
    input_path="en.train.unique_ids_datetime.conll",
    output_path="ru.train.unique_ids.conll",
    start_id="# id: train_1",
    limit=None
)