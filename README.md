# Extractors

![https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png](https://github.com/openschemas/spec-template/raw/master/img/hexagon_square_small.png)

This is a repository with example extractors and recipes intended to be used
with [schemaorg](https://openschemas.github.io/schemaorg/#Usage) Python 
to help you to extract metadata from your datasets,
software and other entities described in [schema.org](https://www.schema.org).


## Specifications

The following specifications have Dockerfiles (and associated Github actions)
for you to use! See the subdirectories to get usage:

 - [Dataset](Dataset) is an example starter script to extract a Dataset.
 - [ImageDefinition](ImageDefinition) is a kind of SoftwareSourceCode extended to describe containers. We provide a Dockerfile that builds the extractor to generate a static page for an input Dockerfile.
 - [ContainerTree](ContainerTree) is an extended ImageDefinition to also include a filesystem listing that can be used to generate a container tree.

For both of the above, when you deploy to Github pages for the first time, you
need to switch Github Pages to deploy from master and then back to the `gh-pages`
branch on deploy. There is a known issue with Permissions if you deploy
to the brain without activating it (as an admin) from the respository first.

## Extractors (without Containers)

The following examples for entities (children of "Thing")
defined in schema.org are also provided. These specifications don't yet have Docker
containers or Github Action extractors.

 - [DataCatalog](DataCatalog): a collection or grouping of Datasets
 - [Organization](Organization): a complete organization, with a ContactPoint
 - [SoftwareSourceCode](SoftwareSourceCode) an example extraction shown [here](https://openbases.github.io/extract-dockerfile/SoftwareSourceCode/) for a Dockerfile.


## What is special about those pages?
For each of the above, the metadata shown is also embedded in the page as json-ld
(when you "View Source.") 

## What files are included in each folder?
Each folder above includes an example python script to extract metadata (`extract.py`), 
a recipe to follow (`recipe.yml`), and the specification in yaml format (in the 
case of a specification not served by production schema.org).

# Usage
For the Docker and Github Actions usage, see inside the [ImageDefinition](ImageDefinition)
folder. For all other schema.org entities and local usage, details are provided here.
Before running these examples, make sure you have installed the module (and note
this module is under development, contributions are welcome!)

```bash
pip install schemaorg
```

To extract a recipe for a particular datatype, you can modify `extract.py` and the 
`recipe.yml` for your particular needs, or use as is. Generally we:

 1. Read in a specific version of the *schemaorg definitions* provided by the library
 2. Read in a *recipe* for a template that we want to populate (e.g., google/dataset)
 3. Use helper functions provided by the template (or our own) to *extract*
 4. Extract, *validate*, and generate the final dataset

The goal of the software is to provide enough structure to help the user (typically a developer)
but not so much as to be annoying to use generally.

## What are the files in each folder?

### recipe.yml Files

If I am a provider of a service and want my users to label their data for my service,
I need to tell them how to do this. I do this by way of a recipe file, in each
example folder there is a file called `recipe.yml` that is a simple listing of required fields defined for the entities that are needed. For example, the [recipe.yml](SoftwareSourceCode/recipe.yml) in the 
"SoftwareSourceCode" folder tells the parser that we need to define
properties for "SoftwareSourceCode" and an Organization or Person. For example.
with the [schemaorg](https://www.github.com/openschemas/schemaorg) Python module 
I can learn that the "SoftwareSourceCode" definition has 121 properties, 
but the recipe tells us that we only need a subset of those
properties for a valid extraction.

### extract.py

This is the code snippet that shows how you extract metadata and use the 
[schemaorg](https://www.github.com/openschemas/schemaorg) Python module
to generate the final template page. This file could be run in multiple places!

 - In a continuous integration setup so that each change to master updates the Github Pages metadata.
 - Using a tool like [datalad](https://datalad.org) that allows for version control of such metadata, and definition of extractors (also in Python).
 - As a Github hook (or action) that is run at any stage in the development process.
 - Rendered by a web server that provides Container Recipes for users that should be indexed with Google Search (e.g., Singularity Hub).

### Dockerfile

For the folders with associated containers, you will find a Dockerfile (and associated entrypoint.sh)! These containers
will build the extractor into an image that can be used with Github Actions.

## Examples

 - [extract-dockerfile Writeup](https://vsoch.github.io/2018/schemaorg/) to demonstrate extraction for a Dockerfile.
 - [extract-dockerfile Repository](https://github.com/openbases/extract-dockerfile)
 - [dockerfiles](https://github.com/openschemas/dockerfiles) A scaled extraction (under development) for ~30-60K Dockerfiles, a subset of the [Dinosaur Dataset](https://vsoch.github.io/datasets/2018/dockerfiles/).


## Resources

 - [Open Container Initative](https://github.com/opencontainers/)
 - [Google Datasets](https://www.blog.google/products/search/making-it-easier-discover-datasets/)
 - [Schemaorg Discussion](https://github.com/schemaorg/schemaorg/issues/2059#issuecomment-427208907)
