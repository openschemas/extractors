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
from schemaorg.logger import bot
from schemaorg.utils import run_command
import json
import tempfile
import os


def run_container_diff(container_name, base=None, output_file=None):
    '''if we dont have a container-diff result from sherlock, try running
       locally'''
    layers = dict()
    response = run_command(["container-diff", "analyze", container_name,
                            "--type=pip", "--type=apt", "--type=history",
                            "--output", output_file, "--json",
                            "--quiet","--verbosity=panic"])
    if response['return_code'] == 0 and os.path.exists(output_file):
        layers = read_json(output_file)
    else:
        if base != None:
            bot.warning('Container name %s not found on Docker Hub, using base %s' %(container_name, base))        
            return run_container_diff(container_name = base, 
                                      output_file=output_file) 
    return layers


def get_tmpfile(prefix=""):
    '''get a temporary file with an optional prefix. By default will be
       created in /tmp By default, the file is closed (and just a name returned).

       Parameters
       ==========
       prefix: prefix the file with this string.

    '''

    # First priority for the base goes to the user requested.
    tmpdir = tempfile.mkdtemp()
    prefix = os.path.join(tmpdir, os.path.basename(prefix))
    fd, tmp_file = tempfile.mkstemp(prefix=prefix) 
    os.close(fd)
    return tmp_file


def extract(dockerfile, contact, container_name=None, output_html=True):
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
    image = Schema(spec_yml)

    # We can obtain these from the environment, or use reasonable defaults
    thumbnail = os.environ.get('IMAGE_THUMBNAIL', 'https://vsoch.github.io/datasets/assets/img/avocado.png')
    about = os.environ.get('IMAGE_ABOUT', 'This is a Dockerfile parsed by the openschemas/extractors container.')
    repository = os.environ.get('GITHUB_REPOSITORY', 'openschemas/extractors')
    description = os.environ.get('IMAGE_DESCRIPTION', 'A Dockerfile build recipe')

    # image.properties
    if len(parser.environ) > 0:
        image.properties['environment'] = parser.environ
    image.properties['entrypoint'] = parser.entrypoint
    image.properties['creator'] = person
    image.properties['version'] = image.version
    image.properties['description'] = description
    image.properties['ContainerImage'] = parser.fromHeader
    image.properties['name'] = container_name

    # Fun properties :)
    image.properties['thumbnailUrl'] = thumbnail
    image.properties['sameAs'] = 'ImageDefinition'
    image.properties['about'] = about
    image.properties['codeRepository'] = 'https://www.github.com/%s' % repository
    image.properties['runtime'] = 'Docker'

    # Generate temporary filename
    output_file = "%s.json" % get_tmpfile("image-definition")

    # Try using container name, if not available default to ContainerImage (FROM)
    layers = run_container_diff(container_name, parser.fromHeader, output_file)

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
    
    if output_html:
        return make_dataset(image)
    return image.dump_json(pretty_print=True)
