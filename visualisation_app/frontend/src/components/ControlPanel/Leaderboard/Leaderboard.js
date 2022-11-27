import React, { useContext, useEffect } from "react";
import { GraphContext } from "../../../App";

export default function Leaderboard() {
  const { graphHook } = useContext(GraphContext);
  const { graph } = graphHook;

  const insert = (newNode, results, index) => {
    const listLength = results.length;
    for (var k = index; k < listLength; k++) {
      if (typeof results[k] !== "undefined") {
        var oldNode = results[k];
        results[k] = newNode;
        newNode = oldNode;
      } else {
        results[k] = newNode;
        return;
      }
    }
    return;
  };

  const addNodeToResults = (newNode, results) => {
    const listLength = results.length;
    const heat = newNode["properties"]["heat"];
    var compareHeat;
    for (var j = 0; j < listLength; j++) {
      if (typeof results[j] !== "undefined") {
        compareHeat = results[j]["properties"]["heat"];
      } else {
        compareHeat = 0;
      }
      if (heat > compareHeat) {
        insert(newNode, results, j);
        return;
      }
    }
    return;
  };

  const getTop5 = (label) => {
    const listLength = 5;
    var results = new Array(listLength);
    var nodes = graph.nodes;
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i]["label"] === label) {
        var newNode = nodes[i];
        addNodeToResults(newNode, results);
      }
    }
    return results;
  };

  useEffect(() => {
    getTop5("Parent");
    getTop5("Person");
  }, []);

  return (
    <div style={{ minWidth: "300px" }}>
      <div
        style={{
          marginTop: "30px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
        }}
      >
        <h4
          style={{
            textAlign: "center",
            color: "#fff",
            fontSize: "14px",
          }}
        >
          Companies Trending
        </h4>
        <div style={{ marginTop: "0" }}>
          <ul
            style={{
              listStyle: "none",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              flexDirection: "column",
              padding: "10px",
            }}
          >
            {getTop5("Parent").map((node, i = 0) => {
              ++i;
              return (
                <li
                  style={{
                    marginTop: "10px",
                    backgroundColor: "#fff",
                    borderRadius: "25px",
                    height: "50px",
                    width: "100%",
                    display: "flex",
                    justifyContent: "left",
                    alignItems: "center",
                    padding: "10px",
                  }}
                >
                  <div
                    style={{
                      backgroundColor: "#0e1f58",
                      width: "30px",
                      height: "30px",
                      borderRadius: "100px",
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                      color: "#fff",
                    }}
                  >
                    <span>{i}</span>
                  </div>
                  <span style={{ marginLeft: "10px" }}>
                    {node.properties.name}
                  </span>
                  <span style={{ marginLeft: "auto", color: "#2090ff" }}>
                    {Math.ceil(node.properties.heat * 1000)} points
                  </span>
                </li>
              );
            })}
          </ul>
        </div>
      </div>
      <div style={{ marginTop: "30px" }}>
        <h4
          style={{
            textAlign: "center",
            color: "#fff",
            fontSize: "14px",
          }}
        >
          People Trending
        </h4>
        <div style={{ marginTop: "0" }}>
          <ul
            style={{
              listStyle: "none",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              flexDirection: "column",
              padding: "10px",
            }}
          >
            {getTop5("Person").map((node, i = 0) => {
              ++i;
              return (
                <li
                  style={{
                    marginTop: "10px",
                    backgroundColor: "#fff",
                    borderRadius: "25px",
                    height: "50px",
                    width: "100%",
                    display: "flex",
                    justifyContent: "left",
                    alignItems: "center",
                    padding: "10px",
                  }}
                >
                  <div
                    style={{
                      backgroundColor: "#ffbe09",
                      width: "30px",
                      height: "30px",
                      borderRadius: "100px",
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                      color: "#fff",
                    }}
                  >
                    <span>{i}</span>
                  </div>
                  <span style={{ marginLeft: "10px" }}>
                    {node.properties.name}
                  </span>
                  <span style={{ marginLeft: "auto", color: "#2090ff" }}>
                    {Math.ceil(node.properties.heat * 1000)} points
                  </span>
                </li>
              );
            })}
          </ul>
        </div>
      </div>
    </div>
  );
}
