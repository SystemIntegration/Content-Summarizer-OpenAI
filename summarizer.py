#!/usr/bin/env python
# -*-coding:utf-8 -*-
#
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
# File          : summarizer.py
# Author        : BMV System Integration Pvt Ltd.
# Version       : 1.0.0
# Date          : 24th January 2023
# Contact       : info@systemintegration.in
# Purpose       : This is the python script to get Summary of the chapter from .epub file.
# import        : openai   - to make the summary of the chapter using AI.
#                 read_pub - A python script to read the .epub file and get chapters from it.
#                 os       - to do os related operations.
#                 math     - for mathematical operations.
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------

import openai
import os
from read_epub import book_to_chapters
import math

dir = os.path.dirname(__file__)
OPENAI_API_KEY_PATH = os.path.join(dir, "OpenAI_apikey.text")
openai.api_key_path = OPENAI_API_KEY_PATH

def chapter_summary(chap_content):

  chap_list = []
  response_list = []
  last_index= 0

  temp_c = chap_content
  if len(chap_content) > 16000 :
    for i in range(math.ceil(len(temp_c)/4000)):
      last_index = str(temp_c[0:4000]).rfind('.')
      chap_list.append(temp_c[0:last_index])
      temp_c = temp_c[last_index+1:-1]
  else:
    chap_list.append(chap_content)

  for chapter_part in chap_list:
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt= "Summarize this chapter : " + chapter_part,
      temperature=0.3,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=1
    )
    response_list.append(str(response["choices"][0]['text']).strip())

  if len(response_list) > 1:
    res_data =""
    for res in response_list:
      res_data += res

      response = openai.Edit.create(
                                model="text-davinci-edit-001",
                                input=res_data,
                                instruction="remove \"this passage....\" and connect all passages properly and do not include word 'Summary' or 'summarized'",
                                temperature=0.5,
                                top_p=1
                              )
    return response['choices'][0]['text']

  else:
    return response_list[0]


if __name__ == "__main__":
  os.system('cls')
  book = input("Enter the path of the book you want summary from : ")
  chapters = book_to_chapters(book)
  chapter_to_read = int(input("There are {} chapters in the book, Enter the number of the chapter for Summarization : ".format(len(chapters))))
  chap_content = chapters[chapter_to_read]['content']
  chapter_name = chapters[chapter_to_read]['name']
  
  print("Summarizing ...........")
  print("If the chapter is too long then it will take time, Please hold ON!!")
  summary = chapter_summary(chap_content=chap_content)
  os.system('cls')
  print("-------------------------------------------------------------------------------------------------------")
  print("Summary of the Chapter {} - {}".format(chapter_to_read, chapter_name), "\n")
  print(summary)
  print("-------------------------------------------------------------------------------------------------------")