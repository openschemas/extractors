# Dataset Extractor

This subfolder builds a container to extract (and optionally deploy) a Dataset
metadata to Github Pages.

# Usage
There are two ways you can use the extractors here!

## Local with Docker

The [Dockerfile](Dockerfile) is built and served on Docker Hub at 
[openschemas/extractors:Dataset](https://cloud.docker.com/u/openschemas/repository/docker/openschemas/extractors). 
Specifically, it will be defined in a Github Actions workflow and then
generate an html page embedded with json-ld, or just the json-ld, to
store with your Dataset. Here is how to generate json-ld output to the console,
and then pipe it into a file:

```bash
# This is a really long name, use an environment variable CID for it
CID=openschemas/extractors:Dataset

# Run using the Dockerfile inside the container (json-ld to terminal)
$ docker run -it ${CID} extract --contact vsoch --name MyDataset --version 1.0.0

# Output html instead (renders into a nice web page)
$ docker run -it ${CID} extract --contact @vsoch --name MyDataset --version 1.0.0 --html

# Pipe into an output file
$ docker run -it ${CID} extract --contact @vsoch --name MyDataset --version 1.0.0 > metadata.json
```

You can (and are encourged) to customize the variables that go into the generation. We
do this by way of environment variables. Here is how to customize the image thumbnail (a web
address), the container description, a more detailed about, and the Github repository.
Note that you can also add [additional arguments](https://schema.org/Dataset) allowed for 
a Dataset with `DATASET_KWARGS`.

```bash
$ docker run -e DATASET_THUMBNAIL=https://vsoch.github.io/datasets/assets/img/avocado.png \
             -e DATASET_ABOUT="This Dockerfile was created by the avocado dinosaur." \
             -e GITHUB_REPOSITORY="openschemas/dockerfiles" \
             -e DATASET_DESCRIPTION="ubuntu with golang and extra python modules installed." \
             -e DATASET_KWARGS="{'encoding' : 'utf-8', 'author' : 'Dinosaur'}" \
             -it openschemas/extractors:Dataset extract --contact vsoch
```

The above variables default to the following:

| Variable | Default | 
|----------|---------|
| DATASET_THUMBNAIL | 'https://vsoch.github.io/datasets/assets/img/avocado.png' |
| DATASET_ABOUT | 'This is a Dataset parsed by the openschemas/extractors container.' |
| GITHUB_REPOSITORY | 'openschemas/extracors' | 
| DATASET_DESCRIPTION | 'A Dataset' |
| DATASET_KWARGS | unset |

Note that if you are using the Github action associated with this repository, `GITHUB_REPOSITORY`
is defined for you (more on this in the next section).

## Github Action

This repository also serves an easy way to generate the file above and deploy
to Github pages! First, set up your `.github/main.workflow` in your repository 
to look like this:

```
workflow "Deploy Dataset Schema" {
  on = "push"
  resolves = ["Extract Dataset Schema"]
}

action "list" {
  uses = "actions/bin/sh@master"
  runs = "ls"
  args = ["/github/workspace"]
}

action "Extract ImageDefinition Schema" {
  needs = ["list"]
  uses = "docker://openschemas/extractors:Dataset"
  secrets = ["GITHUB_TOKEN"]
  env = {
    DATASET_THUMBNAIL = "https://vsoch.github.io/datasets/assets/img/avocado.png"
    DATASET_ABOUT = "Lots and lots of data."
    DATASET_DESCRIPTION = "The best dataset"
  }
  args = ["extract", "--name", "MyDataset", "--contact", "@vsoch", "--version", "1.0.0", "--deploy"]
}
```

 1. In the first block, we define the workflow, and say that it resolves with the last step.
 3. In the second block, this is for debugging. You don't really need it, but it's a sanity check to list the workspace content.
 4. In the final block, we need to set environment variables that we want to change, and then run the container. The `--name` is the name of my Dataset. The `--contact` is also my name. The `--version` is the version for the dataset. The `--deploy` command will upload it to Github pages.

In summary, we have the following variables:

| Variable | Default | 
|----------|---------|
| GITHUB_TOKEN | provided by Github in environemnt as secret |
| DATASET_THUMBNAIL | 'https://vsoch.github.io/datasets/assets/img/avocado.png' |
| DATASET_ABOUT | 'This is a Dockerfile parsed by the openschemas/extractors container.' |
| GITHUB_REPOSITORY | 'openschemas/extracors' (also provided by Github) | 
| DATASET_DESCRIPTION | 'A Dockerfile build recipe' |
| GITHUB_ACTOR | Your Github username (provided by Github, you don't need to set) |
| GITHUB_REPO | The repository (again, provided by Github) |

## Development

If you want to build the image locally, we follow the Docker Hub context rules
and the Dockerfile expects to be built from the [root of the repository](../).
This would then look like this:

```bash
$ docker build -f Dataset/Dockerfile -t openschemas/extractors:Dataset .
```
and if you want to push (because Docker Hub is slow sometimes)

```bash
$ docker push openschemas/extractors:Dataset
```
