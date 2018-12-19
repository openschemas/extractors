# ImageDefinition Extractor

This subfolder builds a container to extract (and optionally deploy) an ImageDefinition.

# Usage
There are two ways you can use the extractors here!

## Local with Docker

The [Dockerfile](Dockerfile) is built and served on Docker Hub at 
[openschemas/extractors:ImageDefinition](). Specifically, it will take an input
Dockerfile, and use container-diff and Singularity Python Client (recipe parser)
to generate an html page embedded with json-ld, or just the json-ld, to
store with your recipe. Here is how to generate json-ld output to the console,
and then pipe it into a file:

```bash
# This is a really long name, use an environment variable CID for it
CID=openschemas/extractors:ImageDefinition

# Run using the Dockerfile inside the container (json-ld to terminal)
$ docker run -it ${CID} extract --contact vsoch

# Output html instead (renders into a nice web page)
$ docker run -it ${CID} extract --contact @vsoch --html

# Run with your own Dockerfile
$ docker run -v $PWD:/data -it ${CID} extract --contact vsoch --filename /data/Dockerfile

# Pipe into an output file
$ docker run -v $PWD:/data -it ${CID} extract --contact vsoch --filename /data/Dockerfile > metadata.json
```

Note that each of these commands will take about 
30 seconds to download the layers (with container-diff) to find software
dependencies. You can also customize some of the variables that go into the generation! We
do this by way of environment variables. Here is how to customize the image thumbnail (a web
address), the container description, a more detailed about, and the Github repository.

```bash
$ docker run -e IMAGE_THUMBNAIL=https://vsoch.github.io/datasets/assets/img/avocado.png \
             -e IMAGE_ABOUT="This Dockerfile was created by the avocado dinosaur." \
             -e GITHUB_REPOSITORY="openschemas/dockerfiles" \
             -e IMAGE_DESCRIPTION="ubuntu with golang and extra python modules installed." \
             -it openschemas/extractors extract --contact vsoch
```

The above variables default to the following:

| Variable | Default | 
|----------|---------|
| IMAGE_THUMBNAIL | 'https://vsoch.github.io/datasets/assets/img/avocado.png' |
| IMAGE_ABOUT | 'This is a Dockerfile parsed by the openschemas/extractors container.' |
| GITHUB_REPOSITORY | 'openschemas/extracors' | 
| IMAGE_DESCRIPTION | 'A Dockerfile build recipe' |


Note that if you are using the Github action associated with this repository, `GITHUB_REPOSITORY`
is defined for you (more on this in the next section).

## Github Action

This repository also serves an easy way to generate the file above and deploy
to Github pages! First, set up your `.github/main.workflow` in your repository 
to look like this:

```
workflow "Deploy ImageDefinition Schema" {
  on = "push"
  resolves = ["Extract ImageDefinition Schema"]
}

action "Extract ImageDefinition Schema" {
  uses = "openschemas/extractors/ImageDefinition@master"
  secrets = ["GITHUB_TOKEN"]
  env = {
    IMAGE_THUMBNAIL = "https://vsoch.github.io/datasets/assets/img/avocado.png"
    IMAGE_ABOUT = "This image smells like parsnips and Santa's socks."
    IMAGE_DESCRIPTION = "ubuntu base with GoLang and custom Python modules"
  }
  args = ["extract", "--contact", "@vsoch", '--deploy']
}
```

Note that we are using the same Docker container as above, but providing the 
entrypoint.sh a `GITHUB_TOKEN` via a secret (it's provided by Github),
along with customizations for the extraction in the environment. I'm also
putting my contact name (@vsoch) as a command line argument, and
running the command with `--deploy`. it will deploy the
static content back to Github pages. In summary, we have the following
variables:

| Variable | Default | 
|----------|---------|
| GITHUB_TOKEN | provided by Github in environemnt as secret |
| IMAGE_THUMBNAIL | 'https://vsoch.github.io/datasets/assets/img/avocado.png' |
| IMAGE_ABOUT | 'This is a Dockerfile parsed by the openschemas/extractors container.' |
| GITHUB_REPOSITORY | 'openschemas/extracors' (also provided by Github) | 
| IMAGE_DESCRIPTION | 'A Dockerfile build recipe' |
| GITHUB_ACTOR | Your Github username (provided by Github, you don't need to set) |
| GITHUB_REPO | The repository (again, provided by Github) |


