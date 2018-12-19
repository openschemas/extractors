#!/usr/bin/env python

'''

Extract metadata from a Dockerfile for a (more detailed) ImageDefinition.

Author: @vsoch
December 18, 2018

This is a "custom" specification (ImageDefinition) that is represented in the 
local file, recipe.yml. It fits into schema.org like this:

    Thing > CreativeWork > SoftwareSourceCode > ImageDefinition

Other suggestions from the OCI Community for fitting names:

    Thing > CreativeWork > SoftwareSourceCode > BuildDefinition
    Thing > CreativeWork > SoftwareSourceCode > BuildInstructions
    Thing > CreativeWork > SoftwareSourceCode > BuildPlan
    Thing > CreativeWork > SoftwareSourceCode > BuildRecipe
    Thing > CreativeWork > SoftwareSourceCode > Configuration
    Thing > CreativeWork > SoftwareSourceCode > ContainerConfig
    Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe

If you want to see the "only production schema.org" example, see
SoftwareSourceCode/extract.py. If you think this categorization is wrong, 
then please speak up! I'll be updating the list here (and the examples that
follow) based on the community feedback. Thanks!

 - https://groups.google.com/a/opencontainers.org/forum/#!topic/dev/vEupyIGtvJs
 - https://github.com/schemaorg/schemaorg/issues/2059#issuecomment-427208907

'''

from schemaorg.templates.google import ( make_person, make_dataset )
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
from schemaorg.utils import read_json
from spython.main.parse import DockerRecipe
from schemaorg.utils import run_command
import json
import os


def run_container_diff(container_name):
    '''if we dont have a container-diff result from sherlock, try running
       locally'''
    layers = dict()
    response = run_command(["container-diff", "analyze", container_name,
                            "--type=pip", "--type=apt", "--type=history",
                            "--json",'--quiet','--verbosity=panic'])
    if response['return_code'] == 0:
        layers = json.loads(response['message'])
    return layers


def extract(dockerfile, contact, output_file=None):
    '''extract a dataset from a given dockerfile, write to html output file.
       Use container-diff and spython to get information about the container.
    '''

    # Step 0. Define absolute paths to our Dockerfile, recipe, output
    here = os.path.abspath(os.path.dirname(__file__))
    recipe_yml = os.path.join(here, "recipe.yml")
    spec_yml = os.path.join(here, "specification.yml")
    
    # Step 1: Show required and recommended fields from recipe
    recipe = RecipeParser(recipe_yml)
    
    # Step 2: Generate a Person (these are Google Helper functions)
    person = make_person(name=contact, description='Dockerfile maintainer')

    # Step 3: Create Dataset
    parser = DockerRecipe(dockerfile)
    container_name = '/'.join(os.path.dirname(dockerfile).split('/')[-2:])
    image = Schema(spec_yml)

    # dataset.properties
    if len(parser.environ) > 0:
        image.properties['environment'] = parser.environ
    image.properties['entrypoint'] = parser.entrypoint
    image.properties['creator'] = person
    image.properties['version'] = image.version
    image.properties['description'] = 'A Dockerfile build recipe'
    image.properties['ContainerImage'] = parser.fromHeader
    image.properties['name'] = container_name

    # Fun properties :)
    image.properties['thumbnailUrl'] = 'https://vsoch.github.io/datasets/assets/img/avocado.png'
    image.properties['sameAs'] = 'ImageDefinition'
    image.properties['about'] = 'This is a Dockerfile parsed by the openschemas/extractors container.'
    image.properties['codeRepository'] = 'https://www.github.com/openschemas/extractors'
    image.properties['runtime'] = 'Docker'

    layers = run_container_diff(container_name)

    if len(layers) > 0:

        # softwareRequirements
        requires = [] # APT and PIP

        # note that the top level key here can be history, files, pip, apt, etc.
        for layer in layers:
        
            ## Pip and Apt will go into softwareRequirements
            if layer['AnalyzeType'] in ["Pip","Apt"]:
                for pkg in layer['Analysis']:
                    requires.append('%s > %s==%s' %(layer['AnalyzeType'],
                                                    pkg['Name'],
                                                    pkg['Version']))         

        image.properties["softwareRequirements"] = requires

    return make_dataset(image, output_file)
