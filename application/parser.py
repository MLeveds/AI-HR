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
"""Summarize the text below into a JSON with exactly the following structure {basic_info: {first_name, last_name, full_name, email, phone_number, location, portfolio_website_url, linkedin_url, github_main_page_url, university, education_level (BS, MS, or PhD), graduation_year, graduation_month, majors, GPA}, work_experience: [{job_title, company, location, duration, job_summary}], project_experience:[{project_name, project_description}]}
"""
       # set up this parser's logger
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
                        model: str = 'GigaChat:latest',
                        temperature: float = 0.0,
                        max_tokens: int = 100,
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
        :param pdf_path: Path to the PDF file.
        :return dictionary of resume with keys (basic_info, work_experience).
        """
        resume = {}
        pdf_str = self.pdf2string(pdf_path)
        print(pdf_str)
        prompt = self.prompt_questions + '\n' + pdf_str

        model = 'GigaChat:latest'
        max_tokens = 4097

        response = self.query_completion(prompt,model=model,max_tokens=max_tokens)
        response_text = response.choices[0].message.content.strip()
        print(response_text)
        resume = json.loads(response_text)
        return resume
