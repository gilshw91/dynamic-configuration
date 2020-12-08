import React from "react";
import ReactDOM from "react-dom";
import MainComponent from "./MainComponent";
import openApiJson from "./openApiJson";

const tagName = "pet$findByTags-3";
const domContainer = document.getElementById(tagName);

// Checks if there is a method name after the service name in the TAG
const elementArray = tagName.split("-");
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
