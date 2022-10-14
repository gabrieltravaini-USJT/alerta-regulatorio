from flask import Blueprint, render_template, request, redirect, url_for
from..extensions import base_alerta
from..models.base import Alerta
import pandas as pd
from datetime import date
from sqlalchemy import desc
import requests

#instanciar a blueprint do site
alertaBp = Blueprint('alertaBp',__name__)


#declaração de rotas (paginas) do site

@alertaBp.route('/teste')
def testebanco():
 
    base_alerta.create_all()
    df_data = {'id' : [1,2,3,4,5,6,7,8,9,10], 
               'titulo':["alerta1","alerta2","alerta3","alerta4","alerta5","alerta6","alerta7","alerta8","alerta9","alerta10"],
               'resumo':["Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit"],
               'link':["www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com"],
               'fonte':['BACEN','BACEN','BACEN','SUSEP','ANS','ANS','SUSEP','ANS',"SUSEP","ANS"],
               'data':[date(2022,10,2),date(2022,10,3),date(2022,10,4),date(2022,4,1),date(2022,9,14),date(2022,6,5),date(2021,3,4),date(2022,9,20),date(2022,7,10),date(2022,1,2)],
               'pldft':[False,False,True,False,False,False,True,False,False,False,]}
    df_teste = pd.DataFrame(data=df_data)

    for index, row in df_teste.iterrows():
        alerta = Alerta(id = row.id, titulo = row.titulo, resumo = row.resumo, link = row.link, fonte = row.fonte, data = row.data, pldft = row.pldft)
        base_alerta.session.add(alerta)
    base_alerta.session.commit()
 
    lista = Alerta.query.order_by(desc(Alerta.data)).all()
    return render_template('teste.html',alerta = lista)