'''
   A service for allow treasure generation for 
   GURPS Dungeon Fantasy per the #8 suppliment.

   Created on Sep 23, 2015

   @author=brian-thomas
   @email=galactictaco@gmail.com

'''
from flask import jsonify, request, render_template, Flask
from gdftg.generator import Generator
import gdftg

# this should reflect both this service and the backing
# assorted libraries
SERVICE_VERSION='v1'

# textmining-ocio library version backing this service
LIBRARY_VERSION = gdftg.version

app = Flask(__name__)

def __generate_treasure(ttype="All", number=1):
    try:
        generator = Generator(ttype)
        return generator.run(numberToGenerate=number, max_item_value=None, min_item_value=None, max_enchantments=None)

    except Exception as ex:
        return str(ex)

@app.route('/')
def home():
    gen = Generator()
    ttypes = sorted(list(gen.treasureClasses()))
    return render_template('home.html', service_version=SERVICE_VERSION, \
                            library_version=LIBRARY_VERSION, \
                            ttypes=ttypes, service_url=request.host)

@app.route('/'+SERVICE_VERSION+'/generate/<int:number>/<ttype>/', methods=['GET'])
def generate_treasure_full(ttype, number):
    return render_template('results.html', items=__generate_treasure(ttype=ttype,number=number))

@app.route('/'+SERVICE_VERSION+'/generate/<int:number>/', methods=['GET'])
def generate_treasure_num_only(number):
    return render_template('results.html', items=__generate_treasure(number=number))

@app.route('/'+SERVICE_VERSION+'/generate/', methods=['GET'])
def generate_treasure_single():
    return render_template('results.html', items=__generate_treasure())

if __name__ == '__main__':
    app.run()

