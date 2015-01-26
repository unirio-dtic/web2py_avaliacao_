from gluon import current

db = DAL('postgres://postgres:devdtic2@sistemas.unirio.br/avaliacao', migrate=False)

kAPIKey = "d694ad743396691552a83008dda6cbf45b28279b23335efbed19fb9a35283035770c8477bb8e812d19b6beac001b2eeb"
current.kAPIKey = kAPIKey

emailPass = 'DuV-zF8-Jek-vqC'
from gluon.tools import Crud

@auth.requires(auth.has_membership('PROGEPE') or auth.has_membership('DTIC'))
def avaliacaoes():
    busca = SQLFORM.grid(
        db.AVAL_ANEXO_1,
        deletable=False,
        editable=False,
        create=False,
        fields=[
            db.AVAL_ANEXO_1.id,
            db.AVAL_ANEXO_1.ANO_EXERCICIO,
            db.AVAL_ANEXO_1.SIAPE_SERVIDOR,
            db.AVAL_ANEXO_1.SIAPE_CHEFIA
        ],
        orderby=db.AVAL_ANEXO_1.DATA_DOCUMENTO,
        paginate=50
    )
    return dict(busca=busca)

@auth.requires(auth.has_membership('PROGEPE') or auth.has_membership('DTIC'))
def naoFinalizadas():
    from gluon.tools import Crud

    crud = Crud(db)

    avaliacaoes = crud.select(db.AVAL_ANEXO_1,
                              db.AVAL_ANEXO_1.CIENTE_SERVIDOR == 'F',
                              fields=[
                                  db.AVAL_ANEXO_1.id,
                                  db.AVAL_ANEXO_1.ANO_EXERCICIO,
                                  db.AVAL_ANEXO_1.SIAPE_SERVIDOR,
                                  db.AVAL_ANEXO_1.SIAPE_CHEFIA
                              ]
    )
    return dict(avaliacoes=avaliacaoes)

@auth.requires(auth.has_membership('PROGEPE') or auth.has_membership('DTIC'))
def gerenciarLista():
    query = db.SUBORDINADOS_EXCLUIR.on(db.SUBORDINADOS_EXCLUIR.TIPO==db.TIPOS_EXCLUSAO.id)

    busca = SQLFORM.grid(
        db.SUBORDINADOS_EXCLUIR,
        left=query,
        deletable=True,
        editable=False,
        create=False,
        fields=[
            db.SUBORDINADOS_EXCLUIR.SIAPE_SERVIDOR,
            db.SUBORDINADOS_EXCLUIR.SIAPE_CHEFIA_TITULAR,
            db.SUBORDINADOS_EXCLUIR.OBSERVACAO,
            db.TIPOS_EXCLUSAO.TIPO
        ],
        orderby=db.SUBORDINADOS_EXCLUIR.id,
        paginate=50
    )
    return dict(busca=busca)