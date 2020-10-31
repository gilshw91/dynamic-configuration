import React from "react";
import ReactDOM from "react-dom";
import MainComponent from "./MainComponent";
import openApiJson from "./openApiJson";

const tagName = "{{TAG-NAME-Placeholder}}";
const domContainer = document.getElementById(tagName);

// Checks if there is a method name after the service name in the TAG
const elementArray = tagName.split("-");
const serviceName = elementArray[0];
const endpointName = elementArray.length > 1 ? elementArray[1] : "";
console.log("serviceName:", serviceName);
ReactDOM.render(
  <MainComponent
    serviceName={serviceName}
    endpointName={endpointName}
    openApiJson={openApiJson}
  />,
  domContainer
);
