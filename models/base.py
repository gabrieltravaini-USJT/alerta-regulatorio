from..extensions import base_alerta


class Alerta (base_alerta.Model):

    __tablename__ = "Alerta"
    id = base_alerta.Column(base_alerta.Integer,primary_key = True, autoincrement = True)
    titulo = base_alerta.Column(base_alerta.String)
    resumo = base_alerta.Column(base_alerta.String)
    link = base_alerta.Column(base_alerta.String)
    fonte = base_alerta.Column(base_alerta.String)
    data = base_alerta.Column(base_alerta.Date)
    pldft = base_alerta.Column(base_alerta.Boolean)

    def __repr__(self):
        return "<Alerta(id = {}, titulo = {}, resumo = {}, link = {}, fonte = {}, data = {}, pldft - {})>".format(self.id,self.titulo,self.resumo,self.link,self.fonte,self.data,self.pldft)