import os
from dotenv import load_dotenv

load_dotenv()
print(os.environ.get('DB_NAME'))

# BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)
# print(os.path.join(BASE_DIR))