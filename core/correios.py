import re
import json
import requests

from bs4 import BeautifulSoup as bs4


def correios(tracking_code) -> dict:
    headers = {
        'Referer': 'https://www2.correios.com.br/sistemas/rastreamento/'}
    data = {
        'objetos': tracking_code,
        'btnPesq': 'Buscar',
        'acao': 'track'}

    res = requests.post(
        'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?',
        data=data,
        headers=headers)

    parser = bs4(res.text, 'html.parser')

    dt_events = parser.find_all('td', {'class': 'sroDtEvent'})
    lb_events = parser.find_all('td', {'class': 'sroLbEvent'})

    regex = re.compile(r'[\n\r\t]')

    eventos = []
    for dt, lb in zip(dt_events, lb_events):
        event = {}
        dt_info = regex.sub(' ', dt.text).split()
        event['data'], event['hora'] = dt_info[:2]
        event['local'] = ' '.join(dt_info[2:])
        event['mensagem'] = ' '.join(regex.sub(' ', lb.text).split())
        eventos.append(event)

    return eventos