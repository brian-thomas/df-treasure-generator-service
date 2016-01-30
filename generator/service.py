'''
   A service for allow treasure generation for 
   GURPS Dungeon Fantasy per the #8 suppliment.

   Created on Sep 23, 2015

   @author=brian-thomas
   @email=galactictaco@gmail.com

'''
from flask import jsonify, request, render_template, Flask
from flask.ext.cors import CORS
from gdftg.generator import Generator
import gdftg
import logging

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 
logging.getLogger(__name__).setLevel(logging.DEBUG)

# this should reflect both this service and the backing
# assorted libraries
SERVICE_VERSION='v1'

# textmining-ocio library version backing this service
LIBRARY_VERSION = gdftg.version

app = Flask(__name__)
CORS(app)

def _abort(code, msg):

    response = jsonify(service_version=SERVICE_VERSION, msg=msg)
    response.status_code = code
    return response

def __generate_treasure(ttype="All", number=1, rformat='json'):
    
    items = []
    try:
        generator = Generator(ttype)
        items = generator.run(numberToGenerate=number, max_item_value=None, min_item_value=None, max_enchantments=None)

    except Exception as ex:
        return str(ex)
    
    if rformat != 'json':
        return render_template('results.html', items = items )
    else:
        return jsonify ( service_version = SERVICE_VERSION,
                         library_version = LIBRARY_VERSION, 
                         items = items.as_list()
                       )

@app.route('/')
def home():
    gen = Generator()
    ttypes = sorted(list(gen.treasureClasses()))
    return render_template('home.html', service_version=SERVICE_VERSION, \
                            library_version=LIBRARY_VERSION, \
                            ttypes=ttypes, service_url=request.host)

@app.route('/'+SERVICE_VERSION+'/generate/<int:number>/<ttype>/', methods=['GET'])
def generate_treasure_full(ttype, number=1, rformat='json'):
    
    rformat = request.args.get('format', 'json')
    return __generate_treasure(ttype=ttype, number=number, rformat=rformat)
            

@app.route('/'+SERVICE_VERSION+'/generate/<int:number>/', methods=['GET'])
def generate_treasure_num_only(number, rformat='json'):
    
    rformat = request.args.get('format', 'json')
    return __generate_treasure(number=number, rformat=rformat)
    
@app.route('/'+SERVICE_VERSION+'/generate/', methods=['GET'])
def generate_treasure_single(rformat='json'):
    rformat = request.args.get('format', 'json')
    return __generate_treasure(rformat=rformat)

@app.route('/'+SERVICE_VERSION+'/ttypes/', methods=['GET'])
def treature_types(rformat='json'):
    
    gen = Generator()
    ttypes = sorted(list(gen.treasureClasses()))
    
    rformat = request.args.get('format', 'json')
    if rformat != 'json':
        return render_template('results.html', items = ttypes)
    else:
        return jsonify(service_version=SERVICE_VERSION, library_version=LIBRARY_VERSION, 
                       treasure_types=ttypes)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    LOG.debug("Flask builtin errorhandler got a 404 abort : "+str(e))
    return _abort(404, "Sorry, Nothing at this URL.")


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    LOG.debug("Flask builtin errorhandler got a 500 abort : "+str(e))
    return _abort(500, 'Sorry, unexpected error: {}'.format(e))

if __name__ == '__main__':
    app.run()

