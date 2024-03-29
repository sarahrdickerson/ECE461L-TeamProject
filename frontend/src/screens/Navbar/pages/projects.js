import React, { useState } from "react";
// import "./projects.css";
import TextField from "@material-ui/core/TextField";
import Button from "@mui/material/Button";
import Inventory from "./inventory.js";
import axios from "../../../api/axios";

function PromptProjects() {
  // const [clicked, setClicked] = useState(false);
  const [showInventory, setShowInventory] = useState(false);
  const [projectName, setProjectName] = useState("");
  const [projectID, setProjectID] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [userName, setUserName] = useState("");
  const [currProjectID, setCurrProjectID] = useState("");

  const handleCreateClick = () => {
    const btn = document.querySelector(".create-button");
    btn.innerHTML = "Creating...";
    btn.setAttribute("disabled", true);
    axios
      .post("/api/createProject", {
        project_name: projectName,
        project_id: projectID,
        users: [localStorage.getItem("username")],
        username: localStorage.getItem("username")
      })
      .then((response) => {
        if (response.data["success"] === true) {
          setUserName(localStorage.getItem("username"));
          localStorage.setItem('projectName', projectName);
          localStorage.setItem('projectID', projectID);
          setShowInventory(true);
        } else {
          if (response.data["message"] === "project id already exists") {
            setErrorMessage(
              "Project ID already exists. Please attempt with a different Project ID."
            );
            btn.removeAttribute('disabled')
            btn.innerHTML = 'Create'
          }
        }
      });
  };

  const handleJoinClick = () => {
    const joinbtn = document.querySelector(".join-button");
    joinbtn.innerHTML = "Joining...";
    joinbtn.setAttribute("disabled", true);
    console.log(localStorage.getItem("username"));
    axios
      .post("/api/joinProject", {
        project_name: projectName,
        project_id: projectID,
        user_id: localStorage.getItem("username"),
        username: localStorage.getItem("username")
      })
      .then((response) => {
        if (response.data["success"] === true) {
          setUserName(localStorage.getItem("username"));
          setShowInventory(true);
          localStorage.setItem('projectName', projectName);
          localStorage.setItem('projectID', projectID);
          window.location.href = "/inventory";
        } else {
          if (response.data["success"] === false) {
            setErrorMessage(
              "Project not found. Please enter a different Project ID or create a new Project."
            );
            joinbtn.removeAttribute('disabled')
            joinbtn.innerHTML = 'Join'
          }
        }
      });
  }

  if (showInventory) {
    return <Inventory/>;
  }

  return (
    <div className="projects-container-wrapper">
      <div className="projects-container">
        <h1>
          <b>Join Project</b>
        </h1>
        <TextField
          id="standard-basic"
          label="Enter Project ID"
          variant="standard"
          className="center-textfield"
          onChange={(event) => setProjectID(event.target.value)}
        />
        <div className="button-container">
          <h1>
            <Button
              className="join-button"
              sx={{
                backgroundColor: "lightgray",
                color: "black",
                textTransform: "none",
                borderRadius: "0",
                width: "100px",
                height: "50px",
                fontSize: "1.2rem",
                marginLeft: "8px",
                fontWeight: "bold",
                textAlign: "center"
              }}
              onClick={handleJoinClick}
            >
              Join
            </Button>
          </h1>
        </div>
        <br />
        <h1>
          <b>Create Project</b>
        </h1>
        <TextField
          id="standard-basic"
          label="Enter Project ID"
          variant="standard"
          className="center-textfield"
          onChange={(event) => setProjectID(event.target.value)}
        />
        <TextField
          id="standard-basic"
          label="Enter Project Name"
          variant="standard"
          className="center-textfield"
          onChange={(event) => setProjectName(event.target.value)}
        />
        <div className="button-container">
          <h1>
            <Button
              className="create-button"
              sx={{
                backgroundColor: "lightgray",
                color: "black",
                textTransform: "none",
                borderRadius: "0",
                width: "100px",
                height: "50px",
                fontSize: "1.2rem",
                marginLeft: "8px",
                fontWeight: "bold",
              }}
              onClick={handleCreateClick}
            >
              Create
            </Button>
          </h1>
        </div>
        {errorMessage && <p>{errorMessage}</p>}
      </div>
    </div>
  );
}

export default PromptProjects;
