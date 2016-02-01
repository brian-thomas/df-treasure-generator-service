'''
   A service for allow treasure generation for 
   GURPS Dungeon Fantasy per the #8 suppliment.

   Created on Sep 23, 2015

   @author=brian-thomas
   @email=galactictaco@gmail.com

'''
from flask import jsonify, request, render_template, send_from_directory, Flask
from flask.ext.cors import CORS
from gdftg.generator import Generator
import os
import gdftg
import logging

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 
#logging.getLogger(__name__).setLevel(logging.DEBUG)

# this should reflect both this service and the backing
# assorted libraries
SERVICE_VERSION='v1'

MAX_ENCHANTMENTS=10

# textmining-ocio library version backing this service
LIBRARY_VERSION = gdftg.version

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

def _abort(code, msg):

    response = jsonify(service_version=SERVICE_VERSION, msg=msg)
    response.status_code = code
    return response

def __generate_treasure(ttype="All", number=1, rformat='json', args=None): 
        
    rformat = args.get('format', 'json')
    max_item_value = args.get('max', None)
    min_item_value = args.get('min', None)
    max_enchantments = args.get('max_enchant', None)
    
    # recast string to int
    if max_item_value:
        max_item_value = int(max_item_value)
        
    if min_item_value:
        min_item_value = int(min_item_value)
    
    if max_enchantments:
        max_enchantments = int(max_enchantments)
        
    # validate our params
    if min_item_value and min_item_value < 0:
        return _abort(400, "Cannot set min item value less than 0")
    
    if max_item_value and max_item_value < 0:
        return _abort(400, "Cannot set max item value less than 0")
        
    if max_enchantments and max_enchantments < 0:
        return _abort(400, "Cannot set max_enchant value less than 0")
    
    if max_enchantments and max_enchantments > MAX_ENCHANTMENTS:
        return _abort(400, "Cannot set max_enchant value greater than "+str(MAX_ENCHANTMENTS))
        
    if min_item_value and max_item_value and max_item_value < min_item_value:
        return _abort(400, "Cannot set min value higher than max value")
    
    items = []
    try:
        generator = Generator(ttype)
        items = generator.run(numberToGenerate=number, 
                              max_item_value=max_item_value, min_item_value=min_item_value, 
                              max_enchantments=max_enchantments)
        
    except Exception as ex:
        return str(ex)
    
    if rformat != 'json':
        return render_template('results.html', items = items )
    else:
        return jsonify ( service_version = SERVICE_VERSION,
                         library_version = LIBRARY_VERSION, 
                         items = items.as_list()
                       )

@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename) #, mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    gen = Generator()
    ttypes = sorted(list(gen.treasureClasses()))
    return render_template('home.html', service_version=SERVICE_VERSION, \
                            library_version=LIBRARY_VERSION, \
                            ttypes=ttypes, service_url=request.host)

@app.route('/v1/generate/<int:number>/<ttype>/')
def generate_treasure_full(ttype, number=1, rformat='json'):
    return __generate_treasure(ttype=ttype, number=number, args=request.args) 
            
@app.route('/v1/generate/<int:number>/')
def generate_treasure_num_only(number, rformat='json'):
    return __generate_treasure(number=number, args=request.args) 
    
@app.route('/v1/generate/')
def generate_treasure_single(rformat='json'):
    return __generate_treasure(args=request.args) 

@app.route('/v1/ttypes/')
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

