import React, { useState } from "react";
import navVideo from "./nav.mp4";
import explorerVideo from "./explorerVideo.mp4";
import filterVideo from "./filterVideo.mp4";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAngleLeft, faAngleRight } from "@fortawesome/free-solid-svg-icons";
import { AiOutlineCloseSquare } from "react-icons/ai";
import { Button, Steps } from "antd";
import s from "./style.module.scss";
const { Step } = Steps;

export default function HowTo(props) {
  const [currentTab, setCurrentTab] = useState(0);

  const shiftLeft = () => {
    if (currentTab > 0) {
      setCurrentTab(currentTab - 1);
    }
  };
  const shiftRight = () => {
    if (currentTab >= 2) {
      props.handleClose();
    } else {
      setCurrentTab(currentTab + 1);
    }
  };

  return (
    <div
      style={{
        position: "absolute",
        width: "100vw",
        height: "130vh",
        zIndex: "2",
        backgroundColor: "rgba(0, 0, 0, 0.9)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: "30px",
          backgroundColor: "white",
          maxWidth: "50%",
          minWidth: "700px",
          height: "700px",
          borderRadius: "5px",
        }}
      >
        <AiOutlineCloseSquare
          style={{
            color: "red",
            fontSize: "30px",
            position: "absolute",
            top: "10px",
            right: "10px",
            cursor: "pointer",
          }}
          onClick={props.handleClose}
        />
        <h2
          style={{
            textAlign: "center",
            margin: "20px 20px",
            marginBottom: "0px",
          }}
        >
          Getting Started
        </h2>
        <Steps
          style={{ width: "70%", margin: "auto" }}
          size="small"
          current={currentTab}
        >
          <Step title="Navigating" />
          <Step title="Exploring" />
          <Step title="Filter" />
        </Steps>
        <div
          style={{
            display: "flex",
            justifyContent: "space-around",
            alignItems: "center",
            padding: "0px 25px",
          }}
        >
          <Button
            type="primary"
            shape="circle"
            icon={<FontAwesomeIcon icon={faAngleLeft} />}
            size={"large"}
            onClick={shiftLeft}
          />
          <div style={{ height: "450px", width: "450px" }}>
            {currentTab === 0 && (
              <video autoPlay muted src={navVideo} width="450" height="500" />
            )}
            {currentTab === 1 && (
              <video
                autoPlay
                muted
                src={explorerVideo}
                width="450"
                height="500"
              />
            )}
            {currentTab === 2 && (
              <video
                autoPlay
                muted
                src={filterVideo}
                width="450"
                height="500"
              />
            )}
          </div>
          <Button
            type="primary"
            shape="circle"
            icon={<FontAwesomeIcon icon={faAngleRight} />}
            size={"large"}
            onClick={shiftRight}
          />
        </div>
        <div className={s.boxStyle}>
          {currentTab === 0 && (
            <p
              style={{ width: "50%", margin: "0px auto", fontWeight: "normal" }}
            >
              <span style={{ color: "blue" }}>Drag to move</span> and{" "}
              <span style={{ color: "blue" }}>scroll to zoom</span>.<br />
              <span style={{ color: "blue" }}>Hover</span> or{" "}
              <span style={{ color: "blue" }}>click</span> nodes to see their
              closest relationships
            </p>
          )}
          {currentTab === 1 && (
            <p
              style={{ width: "50%", margin: "0px auto", fontWeight: "normal" }}
            >
              <span style={{ color: "blue" }}>Hover</span> to explore node
              attributes and <span style={{ color: "blue" }}>search</span> to
              find nodes
            </p>
          )}
          {currentTab === 2 && (
            <p
              style={{ width: "50%", margin: "0px auto", fontWeight: "normal" }}
            >
              <span style={{ color: "blue" }}>Filter</span> based on {" "}
              <span style={{ color: "blue" }}>node types</span>{", "}
              <span style={{ color: "blue" }}>relationship types</span>{" and "}
              <span style={{ color: "blue" }}>recency</span>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
