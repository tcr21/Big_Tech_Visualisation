import React, { useContext } from "react";
import FilterElement from "./FilterElement";
import { GraphContext } from "../../../App";
import s from "./style.module.scss";

export default function Filter() {
  const { nodeHook, linkHook, loadingHook, graphHook, styleHook, dateHook } =
    useContext(GraphContext);
  const { currentNodeTypes, setCurrentNodeTypes } = nodeHook;
  const { currentLinkTypes, setCurrentLinkTypes } = linkHook;
  const { graphLoading, setGraphLoading } = loadingHook;
  const { graph } = graphHook;
  const { nodeStyles } = styleHook;
  const { dateState, setDateState } = dateHook;

  // Turn array into format compatible with React-Select options
  const reactSelectFormatter = (array) => {
    return array.map((element) => ({
      value: `${element}`,
      label: `${element}`,
    }));
  };

  const nodeOptions = reactSelectFormatter(
    Array.from(new Set(graph.nodes.map((node) => node.label)))
  );
  const exclude = [
    "Name",
    "Owners",
    "Subsidiaries",
    "Founders",
    "Board_members",
  ];
  const otherSelectOption = reactSelectFormatter(["Other"])[0];
  const linkOptions = reactSelectFormatter(
    Array.from(
      new Set(
        graph.links
          .filter((link) => !exclude.includes(link.relationship))
          .map((link) => link.relationship)
      )
    ).concat(otherSelectOption.value)
  );

  const handleNodeChange = async (e) => {
    setGraphLoading(true);
    await setCurrentNodeTypes(e);
  };

  const handleLinkChange = async (e) => {
    let modifiedEvent = e.filter((el) => el !== otherSelectOption);
    let otherExcluded = false;
    for (const obj of e) {
      if (obj.value === otherSelectOption.value) {
        otherExcluded = true;
        break;
      }
    }
    setGraphLoading(true);
    if (otherExcluded) {
      await setCurrentLinkTypes(
        reactSelectFormatter(exclude).concat(modifiedEvent)
      );
    } else {
      await setCurrentLinkTypes(modifiedEvent);
    }
  };

  const handleClick = () => {
    setGraphLoading(false);
  };

  const nodeOptionStyles = {
    multiValue: (styles) => {
      return {
        ...styles,
        borderRadius: "100px",
        backgroundColor: "transparent",
        color: "white",
      };
    },
    multiValueLabel: (styles, node) => {
      return {
        ...styles,
        borderRadius: "100px",
        backgroundColor: nodeStyles[node.data.label],
        color: "white",
        border: "1px solid white",
      };
    },
    multiValueRemove: (styles) => {
      return {
        ...styles,
        backgroundColor: "transparent",
        color: "lightgrey",
        padding: "0px",
        ":hover": {
          cursor: "pointer",
        },
      };
    },
  };

  const linkOptionStyles = {
    multiValue: (styles) => {
      return {
        ...styles,
        color: "black",
      };
    },
  };

  const handleDateChange = async (e) => {
    setGraphLoading(true);
    await setDateState(e.target.value);
  };

  const handleDateIncremental = async (e) => {
    setGraphLoading(true);
    if (e.target.innerHTML === "+") {
      await setDateState(dateState + 1);
    } else if (e.target.innerHTML === "-") {
      await setDateState(dateState - 1);
    }
  };

  return (
    <div className={s.container}>
      <FilterElement
        options={nodeOptions}
        placeholder={"Select node types..."}
        defaultValue={currentNodeTypes}
        handleChange={handleNodeChange}
        style={nodeOptionStyles}
        label={"Node Types"}
      />
      <FilterElement
        options={linkOptions}
        placeholder={"Select relationship types..."}
        defaultValue={currentLinkTypes
          .filter((link) => {
            return exclude.includes(link.value) === false;
          })
          .concat(otherSelectOption)}
        style={linkOptionStyles}
        handleChange={handleLinkChange}
        label={"Relationship Types"}
      />
      <div className={s.dateRangeContainer}>
        <h5>Days Since Publishing</h5>
        <form autocomplete="off">
          <div className={s.inputStyles}>
            <div
              style={{
                borderRadius: "100%",
                margin: "0px 10px",
                backgroundColor: "white",
                border: "1px #2090ff solid",
                width: "30px",
                height: "30px",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                cursor: "pointer",
              }}
              onClick={handleDateIncremental}
            >
              <span style={{ fontSize: "20px", color: "#2090ff" }}>-</span>
            </div>
            <input
              style={{
                width: "100px",
                textAlign: "center",
              }}
              value={dateState}
              onChange={handleDateChange}
            />
            <div
              style={{
                borderRadius: "100%",
                margin: "0px 10px",
                backgroundColor: "white",
                border: "1px #2090ff solid",
                width: "30px",
                height: "30px",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                cursor: "pointer",
              }}
              onClick={handleDateIncremental}
            >
              <span style={{ fontSize: "20px", color: "#2090ff" }}>+</span>
            </div>
          </div>
        </form>
      </div>
      <div
        onClick={graphLoading ? handleClick : undefined}
        className={graphLoading ? s.buttonStyle : s.inactiveButtonStyle}
      >
        Apply
      </div>
    </div>
  );
}
