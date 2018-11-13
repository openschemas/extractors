#!/usr/bin/env python

'''
This function will demonstrate how we can generate a DataCatalog
Author: @vsoch
November 13, 2018

    Thing > DataCatalog

'''

from schemaorg.templates.google import make_dataset
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
import os


def extract(name, url, description,
            about=None, thumbnail=None, output_file=None, **kwargs):
    '''extract a DataCatalog to describe some dataset(s). To add more
       properties, just add them via additional keyword args (kwargs)
    
       Parameters
       ==========
       output_file: An html output file to write catalog to (optional)
       url: the url to get the catalog
       name: the name of the DataCatalog
       description: a description of the DataCatalog
       thumbnail: an image thumbnail (web url)
       about: text about the data catalog (optional).
    '''

    # Step 0. Define absolute paths to our Dockerfile, recipe, output
    here = os.path.abspath(os.path.dirname(__file__))
    recipe_yml = os.path.join(here, "recipe.yml")
    
    # Step 3: Create Data Catalog
    catalog = Schema("DataCatalog")

    # Step 1: Show required and recommended fields from recipe
    recipe = RecipeParser(recipe_yml)
    
    # datacatalog.properties
    catalog.add_property('url', about)
    catalog.add_property('name', name)
    catalog.add_property('description', description)
    catalog.add_property('thumbnailUrl', thumbnail)    
    catalog.add_property('about', about)

    # Additional (won't be added if not part of schema)
    for key,value in kwargs.items():
        catalog.add_property(key, value)

    # Step 4: Validate Data Structure
    recipe.validate(catalog)

    # Step 5: If the user wants to write to html, do it before return
    if output_file is not None:
        make_dataset(catalog, output_file)

    return catalog
