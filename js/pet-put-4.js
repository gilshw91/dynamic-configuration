import React from "react";
import ReactDOM from "react-dom";
import MainComponent from "./MainComponent";
//import TestComponent from "./TestComponent";
import openApiJson from "./openApiJson";

const tagName = "pet-put-4";
const domContainer = document.getElementById(tagName);
const elementValue = document.getElementById(tagName).childNodes[0].wholeText;

// Checks if there is a method name after the service name in the TAG
const elementArray = elementValue.split("-");
const serviceName = elementArray[0];
const endpointName = elementArray.length > 1 ? elementArray[1] : "";

ReactDOM.render(
  <MainComponent
    serviceName={serviceName}
    endpointName={endpointName}
    openApiJson={openApiJson}
  />,
  domContainer
);
