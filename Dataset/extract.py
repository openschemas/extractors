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

from schemaorg.templates.google import ( 
    make_dataset, 
    make_person
)
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
import ast
import os
import tempfile


def extract(name, version=None, contact=None, output_html=True,
            description=None, thumbnail=None, sameAs=None, 
            about=None, repository=None):

    ''' extract a Dataset to describe some Github repository. To add more
        properties, just add them via additional keyword args (kwargs)
    
        Parameters
        ==========
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
    email = os.environ.get('DATASET_EMAIL')
    template = os.environ.get('DATASET_TEMPLATE', "google/dataset-table.html")

    # Can be one of:
    # google/dataset-table.html  (bootstrap)
    # google/visual-dataset.html (see vsoch.github.io/zenodo-ml)
    # google/dataset.html        (just blank page, json metadata)
    # google/dataset-vue-table.html
    # see https://openschemas.github.io/schemaorg#7-embed-in-html-with-json-ld

    # Contact metadata
    contact = os.environ.get('GITHUB_ACTOR', contact)
    contact_url = os.environ.get('CONTACT_URL', repository)
    contact_description = os.environ.get('CONTACT_DESCRIPTION', 'Dataset maintainer')    
    contact_type = os.environ.get('CONTACT_TYPE', 'customer support')
    contact_telephone = os.environ.get('CONTACT_TELEPHONE')
    contact = add_kwargs(contact, 'DATASET_DOWNLOAD_KWARGS')

    # Download Link
    download_link = os.environ.get('DATASET_DOWNLOAD_LINK')
    encoding = os.environ.get('DATASET_ENCODING_FORMAT')
    if download != None:
        download = Schema('DataDownload')
        download.add_property('encodingFormat', encoding)
        download.add_property('contentUrl', download_link)
        download = add_kwargs(download, 'DATASET_DOWNLOAD_KWARGS')
        dataset.add_property('distribution', [download])

    # Get the repository full url for contact
    if not contact_url.startswith('http'): 
        contact_url = "https://www.github.com/%s" % contact_url
       
    if contact is not None:
        person = make_person(name=contact, 
                             description=contact_description,
                             url=contact_url,
                             contact_type=contact_type,
                             telephone = contact_telephone)
        person = add_kwargs(person, 'CONTACT_KWARGS')
        dataset.add_property('creator', person)

    # dataset.properties
    dataset.add_property('version', version)
    dataset.add_property('description', description)
    dataset.add_property('name', name)
    dataset.add_property('thumbnailUrl', thumbnail)
    dataset.add_property('about', about)
    dataset = add_kwargs(dataset, 'DATASET_KWARGS')

    # Step 5: Validate Data Structure
    recipe.validate(dataset)
    
    if output_html:
        return make_dataset(dataset, template=template)
    return dataset.dump_json(pretty_print=True)

def add_kwargs(schema, envar):
    '''add key word argumets from the environment to a schema object.
    '''
    KWARGS = os.environ.get(envar) 
    if KWARGS is not None:
        KWARGS = ast.literal_eval(KWARGS)
        for key,value in KWARGS.items():
            schema.add_property(key, value)
    return schema
