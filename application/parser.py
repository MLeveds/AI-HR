from pdfminer.high_level import extract_text as pdftotext
from gigachat import GigaChat
import re
import logging
import json
from tokenizer import num_tokens_from_string

class ResumeParser():
    def __init__(self, API_KEY):
        # set GPT-3 API key from the environment vairable
        # GPT-3 completion questions

        self.prompt_questions = \
'''От тебя требуется только принимать информацию о кандидате на вход и без каких-либо пояснений выдававать JSON в данном формате: 
{
  "resume": {
    "resume_id": "",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "middle_name": "Отчество",
    "birth_date": "дата рождения в формате ГГГГ-ММ-ДД",
    "birth_date_year_only": "",
    "country": "Страна проживания кандидата",
    "city": "Город проживания",
    "about": "Сведения из начала резюме",
    "key_skills": "Основные навыки",
    "salary_expectations_amount": "Ожидаемая заработная плата",
    "salary_expectations_currency": "валюта зарплаты",
    "photo_path": "",
    "gender": "Пол кандидата",
    "language": "родной язык кандидата",
    "resume_name": "Название резюме либо позиция на которую кандидат подаётся",
    "source_link": "",
    "contactItems": [
      {
        "resume_contact_item_id": "",
        "value": "сам контакт",
        "comment": "комментарий к контакту",
        "contact_type": "Типы контактов - contact_type: 1: Телефон, 2: Email, 3: Skype, 4: Telegram, 5: Github; укажи только цифру типа, не пиши сам тип"
      }
    ],
    "educationItems": [
      {
        "resume_education_item_id": "",
        "year": "год окончания образования",
        "organization": "организация",
        "faculty": "факультет",
        "specialty": "специализация",
        "result": "результат образования (красный/синий диплом)",
        "education_type": "Виды образования - education_type: 1: Начальное, 2: Повышение квалификации, 3: Сертификаты, 4: Основное; укажи только цифру типа, не пиши сам тип",
        "education_level": "Уровень образования - education_level: 1: Среднее, 2: Среднее специальное, 3: Неоконченное высшее, 4: Высшее, 5: Бакалавр, 6: Магистр, 7: Кандидат наук, 8: Доктор наук; укажи только цифру типа, не пиши сам тип"
      }
    ],
    "experienceItems": [
      {
        "resume_experience_item_id": "",
        "starts": "начало работы",
        "ends": "окончание работы",
        "employer": "Компания работадатель",
        "city": "город работы",
        "url": "ссылка на работадателя",
        "position": "Название позиции",
        "description": "описание позиции и опыта",
        "order": "порядок следования в массиве опыта работы"
      }
    ],
    "languageItems": [
      {
        "resume_language_item_id": "",
        "language": "язык",
        "language_level": "уровень владения language_level: 1: Начальный, 2: Элементарный, 3: Средний, 4: Средне-продвинутый, 5: Продвинутый, 6: В совершенстве, 7: Родной; укажи только цифру типа, не пиши сам тип"
      }
    ]
  }
}
Заполни JSON согласно информации в резюме, если в резюме нет информации согласно полю, оставь пропуск или вставь логичный ответ (например, если город образования - Москва, значит страну точно можно указать Россия). Значения полей приведены только для информации о полях, не оставляй её в итоговом JSON
'''
        logging.basicConfig(filename='logs/parser.log', level=logging.DEBUG)
        self.logger = logging.getLogger()
        self.api_key = API_KEY
    def pdf2string(self: object, pdf_path: str) -> str:
        """
        Extract the content of a pdf file to string.
        :param pdf_path: Path to the PDF file.
        :return: PDF content string.
        """
        with open(pdf_path, "rb") as f:
            pdf = pdftotext(f)
        pdf_str = "\n\n".join(pdf)
        pdf_str = re.sub('\s[,.]', ',', pdf_str)
        pdf_str = re.sub('[\n]+', '\n', pdf_str)
        pdf_str = re.sub('[\s]+', ' ', pdf_str)
        pdf_str = re.sub('http[s]?(://)?', '', pdf_str)
        return pdf_str

    def query_completion(self: object,
                        prompt: str,
                        model: str = 'GigaChat',
                        temperature: float = 0.0,
                        max_tokens: int = 2000,
                        top_p: int = 1,
                        frequency_penalty: int = 0,
                        presence_penalty: int = 0) -> object:
        """
        Base function for querying GPT-3. 
        Send a request to GPT-3 with the passed-in function parameters and return the response object.
        :param prompt: GPT-3 completion prompt.
        :param model: The model, or model, to generate completion.
        :param temperature: Controls the randomnesss. Lower means more deterministic.
        :param max_tokens: Maximum number of tokens to be used for prompt and completion combined.
        :param top_p: Controls diversity via nucleus sampling.
        :param frequency_penalty: How much to penalize new tokens based on their existence in text so far.
        :param presence_penalty: How much to penalize new tokens based on whether they appear in text so far.
        :return: GPT-3 response object
        """
        self.logger.info(f'query_completion: using {model}')

        #estimated_prompt_tokens = num_tokens_from_string(prompt, model)
        #estimated_answer_tokens = (max_tokens - estimated_prompt_tokens)
        #self.logger.info(f'Tokens: {estimated_prompt_tokens} + {estimated_answer_tokens} = {max_tokens}')

        print(self.api_key)
        client = GigaChat(credentials='NDRlZWI4NjktY2NkYS00MDliLWExYTItZmVmZmVjN2QyM2ZjOjZlNjFiMDg5LTc3YTQtNDdkMS04NjMxLWFlNzVhNDVmNmNjMA==',
                          verify_ssl_certs=False, model=model)
        
        
        response = client.chat(prompt)
        return response
    
    
    def query_resume(self: object, pdf_path: str) -> dict:
        """
        Query GPT-3 for the work experience and / or basic information from the resume at the PDF file path.
        :return dictionary of resume with keys (basic_info, work_experience).
        """
        resume = {}
        pdf_str = self.pdf2string(pdf_path)
        print(pdf_str)
        prompt = self.prompt_questions + '\n' + pdf_str

        model = 'GigaChat'
        max_tokens = 4097

        response = self.query_completion(prompt,model=model,max_tokens=max_tokens)
        response_text = response.choices[0].message.content.strip()
        print(response_text)
        resume = json.loads(response_text)
        return resume