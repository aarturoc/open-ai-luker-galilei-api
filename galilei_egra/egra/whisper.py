from utils import get_current_file_path
import openai
from dotenv import load_dotenv
load_dotenv() 

def main():
    current_file_path = get_current_file_path()
    print(f"El archivo actual se encuentra en: {current_file_path}")


if __name__=="__main__":
    main()