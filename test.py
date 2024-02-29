from pdf_parser import parse_pdf

print(parse_pdf('DataScience_CV_eng.pdf'), file=open('output.txt', 'w'))
