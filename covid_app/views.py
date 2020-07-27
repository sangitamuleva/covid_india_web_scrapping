from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
import pandas as pd
# from .models import Search
from . import models


# Create your views here.

def home(request):
    url = "https://en.wikipedia.org/wiki/COVID-19_pandemic_in_India"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features="html.parser")

    table_list = soup.find('table', class_='infobox')

    rows = table_list.findAll(lambda tag: tag.name == 'tr')
    for i in rows:

        td_tag = i.find('td')
        if i.find('th'):
            if i.find('th').get_text(strip=True) == 'Confirmed cases':
                confirmed_case = i.find('td').get_text(strip=True).split(' ')[0]
                # print(confirmed_case)
            if i.find('th').get_text(strip=True) == 'Active cases':
                active_case = i.find('td').get_text(strip=True).split(' ')[0]
                # print(active_case)
            if i.find('th').get_text(strip=True) == 'Recovered':
                recovered_case = i.find('td').get_text(strip=True).split(' ')[0]
                # print(recovered_case)
            if i.find('th').get_text(strip=True) == 'Deaths':
                death_case = i.find('td').get_text(strip=True).split(' ')[0]
                # print(death_case)

    # table
    rows=html_table()

    context = {"c": confirmed_case, "r": recovered_case, "a": active_case, "d": death_case,"row":rows}
    return render(request, 'main.html', context)


def html_table():
    url = "https://en.wikipedia.org/wiki/COVID-19_pandemic_in_India"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features="html.parser")
    # print(soup.prettify())

    div_table = soup.find(id='covid19-container')
    # print(div_table)
    data = div_table.tbody
    # print(data)

    row1 = dict()
    for i in data.findAll('tr'):
        # print('-------')
        # print(i)
        td_num=[]
        if i.find('th'):
            th_tags = i.find('th')
            state_name = th_tags.get_text(strip=True)
            # print(state_name)

        if i.find('td'):
            td_num = [d.get_text(strip=True) for d in i.findAll('td')]
            # print(td_num)

        if len(td_num) > 1:
            row1.update({state_name : td_num})
    # print(row1)

    return row1