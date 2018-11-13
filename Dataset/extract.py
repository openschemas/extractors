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

from schemaorg.templates.google import make_dataset
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
from spython.main.parse import DockerRecipe
import os


def extract(name, description, version, thumbnail, sameAs, 
            about=None, output_file=None, person=None, catalog=None,
            **kwargs):

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
    
    # Step 1: Show required and recommended fields from recipe
    recipe = RecipeParser(recipe_yml)
   
    # Step 3: Create Dataset
    dataset = Schema("Dataset")

    # dataset.properties
    dataset.add_property('creator', person)
    dataset.add_property('version', version)
    dataset.add_property('description', description)
    dataset.add_property('name', name)
    dataset.add_property('thumbnailUrl', thumbnail)
    dataset.add_property('sameAs', sameAs)
    dataset.add_property('about', about)

    # Additional (won't be added if not part of schema)
    for key,value in kwargs.items():
        dataset.add_property(key, value)

    # Add dataCatalog
    dataset.add_property('includedInDataCatalog', catalog)

    # Step 4: Validate Data Structure
    recipe.validate(dataset)

    # Step 5: Optionally output to file
    if output_file is not None:
        make_dataset(dataset, output_file)
    return dataset
