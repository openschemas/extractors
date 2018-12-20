#!/bin/bash

# This is the deploy script (to Github pages) that is run by the entrypoint, 
# given that the user has specified --deploy and GITHUB_TOKEN is found
# in the environment. The script requires the token, and a filename to deploy
# (should be index.html). This script is intended to be used with Github
# actions, so the various GITHUB_* variables should be defined.

DEPLOY_FILE="${1:-}"

if [ ! -f "${DEPLOY_FILE}" ]; then
    echo "Cannot find ${DEPLOY_FILE}";
    exit 1;
fi

echo "Deploy File is ${DEPLOY_FILE}"

# Set up variables for remote repository and branch
REMOTE_REPO="https://${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
REMOTE_BRANCH="gh-pages"

# Initialize Github Pages and push
git init && \
    git config user.name "${GITHUB_ACTOR}" && \
    git config user.email "${GITHUB_ACTOR}@users.noreply.github.com" && \

    # Checkout orphan branch, we remove all because can't add main.workflow
    git checkout gh-pages || git checkout --orphan gh-pages
    git rm -rf .

    # Add the deploy file to the PWD, an empty github pages
    cp ${DEPLOY_FILE} .
    git add $(basename "${DEPLOY_FILE}");

    # Push to Github pages
    git commit -m 'Automated deployment to Github Pages: Action deploy' --allow-empty && \
    git push origin gh-pages && \
    echo "Successful deploy."
