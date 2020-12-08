import os
import sys
import argparse
from datetime import datetime
import requests
import json
import os.path
# ===================================================================
# Script name : analyze-tags.py
# Description : Replace every TAG in the HTML files within the provided source folder with it's compatible React
#               Component - which builds and displays UI from the swagger
# Input: Source folder and swagger as JSON (provided as URL or as file). optional inputs are the target folder and
#        a template folder
# Output: New HTML files contains connection to their React component, JS files and JSON file
# Author : Gil Shwartz
# ===================================================================
# Global variables
logFilePath = "analyze-tags.log"
prefix = '@#@'
targetHTMLFolder = "./dynamic_config_html/"
targetJSFolder = "./dynamic_config_js/"
templateFolderPath = "./dynamic_config_templates/"
# ===================================================================
# Function: log
# Synopsis: Write application events to an external log file
# Return value: None
# ===================================================================


def log(message, type="info"):
    print(f"{type.upper()}: {message}")
    logFile = open(logFilePath, "a")
    logFile.write(f"{datetime.now()}\t{type.upper()}\t{message}\n")
    logFile.close()
# ===================================================================
# Function: clearLog
# Synopsis: Delete the log in every new instance of the script
# Return value: None
# ===================================================================


def clearLog():
    if os.path.exists(logFilePath):
        try:
            os.remove(logFilePath)
        except OSError as e:
            log(f"Failed deleting log file {logFilePath}: {e}", "error")
# ===================================================================
# Function: parseArgs
# Synopsis: Parse the provided command-line arguments
# Return value: Namespace(...args)
# ===================================================================


def parseArgs():
    parser = argparse.ArgumentParser(prog="Analyze Tags")
    parser.add_argument('--src-dir', required=True,
                        help='Source directory path')
    parser.add_argument(
        '--json-path', help='A full path of the OpenApi v2 JSON file (required if no --url is specified)')
    parser.add_argument(
        '--url', help='An OpenApi v2 specification URL to fetch the JSON from (required if no --json-path is specified)')
    parser.add_argument(
        '--log-path', help="The full path of the log file to write [Default: current folder]")
    parser.add_argument(
        '--target-path', help='A full path of the target folder where the cloned HTML files will be saved'
                              ' [Default: current folder]')
    return parser.parse_args()
# ===================================================================
# Function: validateArgs
# Synopsis: Validate the provided user arguments
# Return value: None
# ===================================================================


def validateArgs(args):
    # validate whether --json-path or --url are specified
    if args.json_path is None and args.url is None:
        log("You must specified at least one of the following arguments: --url or --json-path", "error")
        exit(-1)
    # validate both --json-path and --url are not provided
    if args.json_path is not None and args.url is not None:
        log("You are not allowed to provide both --url and --json-path. Please remove one of the above", "error")
        exit(-1)
    # validate --src-dir is exists if specified
    if args.src_dir is not None:
        if not (os.path.exists(args.src_dir)):
            log(f"The source folder '{args.src_dir}' does not exists!", "error")
            exit(-1)
    # validate --json-path is exists if specified
    if args.json_path is not None:
        if not (os.path.exists(args.json_path)):
            log(f"JSON file '{args.json_path}' does not exists!", "error")
            exit(-1)
# ===================================================================
# Function: replaceTagInDOMElement
# Synopsis: get an HTML string, search tag and replace it with <div>
# Return value: the service name
# ===================================================================


def replaceTagInDOMElement(currentHTML, index, templateFile):
    """Gets HTML string and returns:
     - the service name,
     - the HTMLs' content after replacing the TAG with 'div' and 'src' elements
     - the template (JS) file
     - the TAG which has replaced"""

    serviceName = ""
    clonedTemplate = ""
    tagName = ""
    if prefix in currentHTML:
        # get the start index of the TAG
        indexOfTag = currentHTML.index(prefix)
        # extract the service name from the tag
        serviceName = currentHTML[indexOfTag::].split(prefix)[1]
        # isServiceExistInJson(serviceName, JSON) --- validate if service exist
        indexOfServiceEnds = indexOfTag + \
            len(prefix) + len(serviceName) + len(prefix)
        # check if there is a method name after the final char of the tag. (alpha char and not </ or \n....)
        if currentHTML[indexOfServiceEnds].isalpha():
            # assuming that afetr the TAG will be a new line
            lengthOfTagWithMethod = len(
                (currentHTML[indexOfTag::].split(prefix)[2]).split("\n")[0])
            tagFound = currentHTML[indexOfTag:indexOfServiceEnds +
                                   lengthOfTagWithMethod]
        else:
            tagFound = currentHTML[indexOfTag:indexOfServiceEnds]
        methodName = tagFound.split(prefix)[-1].strip()
        if methodName is not "":
            tagName = f"{serviceName}-{methodName}"
            tagName = tagName.replace(
                "/", "$").replace("{", "!").replace("}", "!")
        else:
            tagName = f"{serviceName}"
            tagName = tagName.replace(
                "/", "$").replace("{", "!").replace("}", "!")
        currentHTML = currentHTML.replace(
            tagFound, f"<div id='{tagName}-{index}'>'Loading...'</div><script src='../dynamic_config_js/{tagName}-{index}.js'></script>", 1)
        clonedTemplate = templateFile.replace(
            "{{TAG-NAME-Placeholder}}", f"{tagName}-{index}")
        tagName = tagName + "-" + str(index)
    return serviceName, currentHTML, clonedTemplate, tagName


# ===================================================================
# Main code
# ===================================================================

# parse inputs arguments
args = parseArgs()
# validate arguments
validateArgs(args)
# set the current instance log path if specified
if args.log_path is not None:
    logFilePath = args.log_path
# recycle current log
clearLog()
# print script has started message
log("Script has started")
# init the path to the target folder if provided
if args.target_path is not None:
    targetHTMLFolder = args.target_path
# initialize the specific json with the specific service
subSwagger = {}
# check if URL is provided and if so, convert the data to JSON.
if args.url:
    res = requests.get(args.url)
    # check if the response from url is valid JSON
    try:
        # parse to json
        swaggerJson = requests.get(args.url).json()
    except ValueError as err:
        log(f"The URL '{args.url}' is not a valid JSON!", "error")
        exit(-1)
else:
    json_path = args.json_path
    # check if the given file is valid JSON
    try:
        swaggerJson = open(json_path)
        swaggerJson = json.loads(swaggerJson.read())
    except ValueError as err:
        log(f"The file '{args.json_path}' is not a valid JSON!", "error")
        exit(-1)

index = 0
# loop over the files in the source folder
for root, dirs, files in os.walk(args.src_dir):
    templateFile = open(templateFolderPath + "template.js").read()
    for fileName in files:
        # loop only on html\htm files
        if fileName.endswith(".html") or fileName.endswith(".htm"):
            currentHTML = open(args.src_dir + '\\' + fileName).read()
            log(f"Working on {fileName}")
            # check if prefix exist in the current file
            if prefix in currentHTML:
                # get the start index of the TAG
                indexOfTag = currentHTML.index(prefix)
                # loop while there is still has Tags in the HTML
                while True:
                    # extract the service name from the tag, the HTML after replacing Tags to divs and the Tag itself
                    serviceName, currentHTML, requestTemplate, methodName = replaceTagInDOMElement(
                        currentHTML, index, templateFile)
                    if not serviceName:
                        break
                    index += 1
                    # saving each cloning template file in the js folder
                    nameOfTemplate = os.path.join(
                        targetJSFolder, methodName + '.js')
                    clonedTemplate = open(nameOfTemplate, 'w')
                    clonedTemplate.write(requestTemplate)
                    clonedTemplate.close()
                # saving each cloning HTML file in the target folder
                nameOfFile = os.path.join(targetHTMLFolder, fileName)
                cloneHTML = open(nameOfFile, 'w')
                cloneHTML.write(currentHTML)
                cloneHTML.close()

# saving the provided swagger
cloneSwagger = open(targetJSFolder + "openApiJson.json", 'w')
cloneSwagger.write(json.dumps(swaggerJson))
cloneSwagger.close()
