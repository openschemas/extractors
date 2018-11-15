#!/usr/bin/env python

'''
This function will demonstrate how we can generate an Organization
Author: @vsoch
November 14, 2018

    Thing > Organization

'''


from schemaorg.templates.google import make_dataset
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
import os


def extract(name, url, telephone,
            email, output_file=None, contact_type="customer_service", 
            **kwargs):
    ''' extract an Organization. Some of the fields required are for
        a "ContactPoint" included within.
 
        Parameters
        ==========
        output_file: An html output file to write catalog to (optional)
        url: the url to get the catalog
        name: the name of the DataCatalog
        contact_type: the type of contact for the ContactPoint
        telephone: the telephone of the ContactPoint
        email: the email of the ContactPoint
    '''

    # Step 0. Define absolute paths to our Dockerfile, recipe, output
    here = os.path.abspath(os.path.dirname(__file__))
    recipe_yml = os.path.join(here, "recipe.yml")

    # Step 2: Create Contact Point    
    contact = Schema("ContactPoint")
    contact.add_property('contactType', contact_type)
    contact.add_property('telephone', telephone)
    contact.add_property('email', email)

    # Step 3: Show required and recommended fields from recipe
    recipe = RecipeParser(recipe_yml)
    
    # Organization properties
    org = Schema("Organization")
    org.add_property('contactPoint', contact)
    org.add_property('url', url)
    org.add_property('name', name)

    # Additional (won't be added if not part of schema)
    for key,value in kwargs.items():
        org.add_property(key, value)

    # Step 4: Validate Data Structure
    recipe.validate(org)

    # Step 5: If the user wants to write to html, do it before return
    if output_file is not None:
        make_dataset(org, output_file)

    return org
