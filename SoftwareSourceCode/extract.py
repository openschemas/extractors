#!/usr/bin/env python

'''
This script will provide a function for extracting information from for
some SoftwareSourceCode. You can optionally provide a Person to the function.

Author: @vsoch
October 21, 2018

    Thing > CreativeWork > SoftwareSourceCode

'''


from schemaorg.templates.google import make_dataset
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
import os

def extract(name, description, thumbnail=None, sameAs=None, version=None,
            about=None, output_file=None, person=None, repository=None,
            runtime=None, **kwargs):

    ''' extract a SoftwareSourceCode to describe a codebase. To add more
        properties, just add them via additional keyword args (kwargs)
    
        Parameters
        ==========
        output_file: An html output file to write catalog to (optional)
        url: the url to get the catalog
        name: the name of the DataCatalog
        description: a description of the DataCatalog
        thumbnail: an image thumbnail (web url)
        about: text about the data catalog (optional).
        version: the software version. If not provided, uses schemarg version
    '''

    # Step 0. Define absolute paths to our Dockerfile, recipe, output
    here = os.path.abspath(os.path.dirname(__file__))
    recipe_yml = os.path.join(here, "recipe.yml")
    
    # Step 1: Show required and recommended fields from recipe
    recipe = RecipeParser(recipe_yml)
    
    # Step 2: Create SoftwareSourceCode
    ssc = Schema("SoftwareSourceCode")

    # dataset.properties
    ssc.add_property('creator', person)
    ssc.add_property('version', version or ssc.version)
    ssc.add_property('description', description)
    ssc.add_property('name', name)
    ssc.add_property('thumbnailUrl', thumbnail)
    ssc.add_property('sameAs', sameAs)
    ssc.add_property('about', about)
    ssc.add_property('codeRepository', repository)
    ssc.add_property('runtime', runtime)

    # Step 3: Additional (won't be added if not part of schema)
    for key,value in kwargs.items():
        ssc.add_property(key, value)

    # Step 4: Validate Data Structure
    recipe.validate(ssc)

    # Step 5: If the user wants to write to html, do it before return
    if output_file is not None:
        make_dataset(ssc, output_file)

    return ssc
