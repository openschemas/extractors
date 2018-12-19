#!/bin/bash

usage () {

    echo "Usage:


         docker run <container> [help|extract]

         Commands:

                help: show help and exit
                extract: extract a json-ld or html page for a specific schema.org
                         data type, from a Dockerfile
         
         Options [extract]:

                --contact | -c the name to add as the maintainer / contact
                --name|-n:     the name of the container for the Dockerfile
                -f|--filepath: specify a Dockerfile path (other than Dockerfile)
                --html         output html instead

         Examples:

              docker run <container> extract ImageDefinition
              docker run <container> extract ImageDefinition --html
              docker run <container> extract ImageDefinition -f /path/to/Dockerfile

         "
}

if [ $# -eq 0 ]; then
    usage
    exit
fi

EXTRACTION="no"
DOCKERFILE="Dockerfile"
OUTPUT_FORMAT="json"
CONTAINER_NAME=""

while true; do
    case ${1:-} in
        -h|--help|help)
            usage
            exit
        ;;
        --extract|extract|-e)
            shift
            EXTRACTION="yes"
        ;;
        --filename|-f)
            shift
            DOCKERFILE="${1:-}"
            shift
        ;;
        --contact|-c)
            shift
            MAINTAINER="${1:-}"
            shift
        ;;
        --html|html)
            shift
            OUTPUT_FORMAT="html"
        ;;
        --name|-n)
            shift
            CONTAINER_NAME="${1:-}"
            shift
        ;;
        -*)
            echo "Unknown option: ${1:-}"
            exit 1
        ;;
        *)
            break
        ;;
    esac
done

EXTRACTION_TYPE=${1:-Dataset}

if [ -z "${MAINTAINER}" ]; then
    echo "Please provide a --contact for the contact."
    exit 1;
fi

# Are we doing an extraction?

if [ "${EXTRACTION}" == "yes" ]; then

    # Does the Dockerfile exist?
    if [ ! -f "${DOCKERFILE}" ]; then
        echo "${DOCKERFILE} does not exist.";
        exit 1;
    fi


    # If the folder doesn't exist, not a valid extraction type
    if [ ! -d "${EXTRACTION_TYPE}" ]; then
        echo "${EXTRACTION_TYPE} is not a valid extraction type.";
        exit 1;
    fi

    # Do the extraction
    python3 run.py "${DOCKERFILE}" "${OUTPUT_FORMAT}" "${MAINTAINER}" "${CONTAINER_NAME}"

else
    echo "Please select an action (e.g., docker run <container> extract <options>)"
fi
