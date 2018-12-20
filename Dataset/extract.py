#!/usr/bin/env python

'''
This function will demonstrate how we can extract metadata for a Dataset
and then generate a (html) web template to serve with it so that it is
able to be indexed by Google Datasets as a Dataset. You can (optionally) 
generate a person and a DataCatalog first.

Author: @vsoch
November 11, 2018

    Thing > Dataset

'''

from schemaorg.templates.google import ( make_dataset, make_person )
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
import ast
import os
import tempfile

def get_tmpfile(prefix=""):
    '''get a temporary file with an optional prefix. By default will be
       created in /tmp By default, the file is closed (and just a name returned).

       Parameters
       ==========
       prefix: prefix the filename with this string.
    '''

    # First priority for the base goes to the user requested.
    tmpdir = tempfile.mkdtemp()
    prefix = os.path.join(tmpdir, os.path.basename(prefix))
    fd, tmp_file = tempfile.mkstemp(prefix=prefix) 
    os.close(fd)
    return tmp_file


def extract(name, version=None, contact=None, output_html=True,
            output_file=None, description=None, thumbnail=None, sameAs=None, 
            about=None, repository=None):

    ''' extract a Dataset to describe some Github repository. To add more
        properties, just add them via additional keyword args (kwargs)
    
        Parameters
        ==========
        output_file: An html output file to write catalog to (optional)
        url: the url to get the catalog
        name: the name of the DataCatalog
        contact: name of a person that is in charge of the dataset
        description: a description of the DataCatalog
        thumbnail: an image thumbnail (web url)
        about: text about the data catalog (optional).
    '''

    # Step 0. Define absolute paths to our Dockerfile, recipe, output
    here = os.path.abspath(os.path.dirname(__file__))
    recipe_yml = os.path.join(here, "recipe.yml")
    
    # Step 1: Show required and recommended fields from recipe
    recipe = RecipeParser(recipe_yml)
   
    # Step 2: Create Dataset
    dataset = Schema("Dataset")

    # We can obtain these from the environment, or use reasonable defaults
    thumbnail = os.environ.get('DATASET_THUMBNAIL', thumbnail or 'https://vsoch.github.io/datasets/assets/img/avocado.png')
    about = os.environ.get('DATASET_ABOUT', about or 'This is a Dataset parsed by the openschemas/extractors container.')
    repository = os.environ.get('GITHUB_REPOSITORY', repository or 'openschemas/extractors')
    description = os.environ.get('DATASET_DESCRIPTION', 'A Dataset')
    email = os.environ.get('DATASET_EMAIL', )

    # Contact metadata
    contact = os.environ.get('GITHUB_ACTOR', contact)
    contact_url = os.environ.get('CONTACT_URL', repository)
    contact_description = os.environ.get('CONTACT_DESCRIPTION', 'Dataset maintainer')    
    contact_type = os.environ.get('CONTACT_TYPE', 'customer support')
    contact_telephone = os.environ.get('CONTACT_TELEPHONE')

    # Get the repository full url for contact
    if not contact_url.startswith('http'): 
        contact_url = "https://www.github.com/%s" % contact_url
       
    if contact is not None:
        person = make_person(name=contact, 
                             description=contact_description,
                             url=contact_url,
                             contact_type=contact_type,
                             telephone = contact_telephone)
        dataset.add_property('creator', person)

    # dataset.properties
    dataset.add_property('version', version)
    dataset.add_property('description', description)
    dataset.add_property('name', name)
    dataset.add_property('thumbnailUrl', thumbnail)
    dataset.add_property('about', about)

    # Step 4: Additional (won't be added if not part of schema)
    DATASET_KWARGS=os.environ.get('DATASET_KWARGS') 
    if DATASET_KWARGS is not None:
        DATASET_KWARGS=ast.literal_eval(DATASET_KWARGS)
        for key,value in DATASET_KWARGS.items():
            dataset.add_property(key, value)

    # Step 5: Validate Data Structure
    recipe.validate(dataset)

    # Generate temporary filename
    output_file = "%s.json" % get_tmpfile("dataset")
    
    if output_html:
        return make_dataset(dataset)
    return dataset.dump_json(pretty_print=True)
