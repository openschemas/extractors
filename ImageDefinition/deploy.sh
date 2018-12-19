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

# Copy the deploy file to $PWD
cp ${DEPLOY_FILE} ${PWD}
DEPLOY_FILE=$(basename "${DEPLOY_FILE}")

# Set up variables for remote repository and branch
REMOTE_REPO="https://${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
REMOTE_BRANCH="gh-pages"

# Initialize Github Pages and push
git init && \
    git config user.name "${GITHUB_ACTOR}" && \
    git config user.email "${GITHUB_ACTOR}@users.noreply.github.com" && \
    git add "${DEPLOY_FILE}" && \
    git commit -m 'action deploy' > /dev/null 2>&1 && \
    git push --force "${REMOTE_REPO}" master:${REMOTE_BRANCH} > /dev/null 2>&1 && \
    rm -fr .git && \
    cd ../ && \
    echo "Successful deploy."
