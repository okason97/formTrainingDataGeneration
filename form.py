from __future__ import print_function

def page_break(id, title):
    dic = {
        "createItem": {
            "item": {
                'itemId': id, 
                'pageBreakItem': {}, 
                'title': title
            },
            "location": {
                "index": 0
            }
        }
    }
    return dic

def scale_question(low, high, lowLabel, highLabel, title = None, uri=None):

    dic = {
        "createItem": {
            "item": {
                "questionItem": {
                    "question": {
                        "required": True,
                        'scaleQuestion': {
                            'low': low, 
                            'high': high, 
                            'lowLabel': lowLabel, 
                            'highLabel': highLabel
                        }
                    },
                },
            },
            "location": {
                "index": 0
            }
        }
    }

    if title:
        dic['createItem']['item']['title'] = title

    if uri:
        dic['createItem']['item']['questionItem']['image'] = {
            'sourceUri': uri, 
            'properties': {
                'alignment': 'CENTER', 'width': 256
            }
        }

    return dic

def view_form(service, id):
    # Prints the form
    return service.forms().get(formId=id).execute()

def create_form(service, imgs_uri):
    # Request body for creating a form
    NEW_FORM = {
        "info": {
            "title": "Verificación de señas generadas",
        }
    }

    UPDATE_FORM_INFO = {
        "updateFormInfo": {
            "info": {
                "title": "Verificación de señas generadas",
                "description": "El objetivo de este formulario es evaluar la calidad de las imágenes generadas en comparación a las imágenes reales. Se le asignará a cada imagen un puntaje del 1 al 5 en realismo, anatomia de los dedos (sus deformaciones) y sus posiciones."
            },
            'updateMask': '*'
        }
    }

    request_list = [UPDATE_FORM_INFO]
    for uri, i in zip(imgs_uri, range(len(imgs_uri))):
        request_list.append(page_break('{0:x}{1}'.format(i,0), 'Imagen {}'.format(i)))
        id_errores = '{0:x}{1}'.format(i,1)
        request_list.append(scale_question(1,5,
                    'No es una mano',
                    'Es mano realista',
                    'Puntúe el nivel de realismo de la siguiente imagen',
                    uri))
        request_list.append(scale_question(1,5,
                    'Dedos anatomicamente incorrectos',
                    'Dedos anatomicamente correctos'))
        request_list.append(scale_question(1,5,
                    'Dedos en posiciones irrealistas',
                    'Dedos en posiciones realistas'))

    # Request body to add a multiple-choice question
    NEW_QUESTION = {
        "requests": list(reversed(request_list))
    }

    # Creates the initial form
    result = service.forms().create(body=NEW_FORM).execute()

    # Adds the question to the form
    service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()