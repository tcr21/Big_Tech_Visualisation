import React, { useEffect, useState, useContext } from "react";
import { GraphContext } from "../../App";
import * as d3 from "d3";
import s from "./style.module.scss";
import ControlPanel from "../../components/ControlPanel/ControlPanel";
import HowTo from "../../components/HowTo/HowTo";

// Updated when node is clicked to store highlighted nodes
var nodeClicked = false;
var highlightNodes = [];

function Visualisation() {
  const {
    nodeHook,
    linkHook,
    loadingHook,
    graphHook,
    styleHook,
    dateHook,
    showHowToHook,
  } = useContext(GraphContext);
  const { currentNodeTypes } = nodeHook;
  const { currentLinkTypes } = linkHook;
  const { graphLoading } = loadingHook;
  const { graph } = graphHook;
  const { nodeStyles } = styleHook;
  const { dateState } = dateHook;
  const { showHowTo, setShowHowTo } = showHowToHook;
  const [currentNode, setCurrentNode] = useState(null);
  const [currentNodeColor, setCurrentNodeColor] = useState("");

  const handleClose = () => {
    setShowHowTo(false);
  };

  // Get up to 3 lines for expanded node tooltip
  const getTooltip = (string, size) => {
    // If node is supposed to be small, max line length is 10, else 15
    const maxLineLength = 10;
    const maxLineNumber = 3;
    if (string.length <= maxLineLength) {
      return [string];
    }

    const splitStr = string.split(" ");
    const lines = [];

    let lineNumber = 0;
    let i = 0;

    while (lineNumber < maxLineNumber && i < splitStr.length) {
      var line = splitStr[i];
      ++i;

      // while under 10 chars, keep adding
      while (
        i < splitStr.length &&
        splitStr[i].length + line.length + 1 <= maxLineLength
      ) {
        line = line + " " + splitStr[i];
        ++i;
      }

      // make third line a substring if we haven't included all words
      if (lineNumber === maxLineNumber - 1 && i < splitStr.length) {
        line = line + "...";
      }

      lines.push(line);
      ++lineNumber;
    }

    return lines;
  };

  const getWrappedNodeLabel = (d) => {
    d[0].forEach((item) => {
      var label = d3.select(item);
      var name = item.__data__.properties.name;

      const lines = getTooltip(name, "small");
      const yTranslate = ((lines) => {
        switch (lines.length) {
          case 1:
            return [0];
          case 2:
            return [-6, 6];
          case 3:
            return [-12, 0, 12];
          default:
            return [0];
        }
      })(lines);

      lines.forEach((line, i) => {
        label
          .append("text")
          .text(() => line)
          .attr("class", `nodeLabel ${item.__data__.label}`)
          .attr("dx", 0)
          .attr("dy", ".35em")
          .style("font-size", "5px")
          .attr("transform", `translate(0, ${yTranslate[i]})`)
          .attr("text-anchor", "middle")
          .transition()
          .duration(300)
          .style("font-size", "10px");
      });
    });
  };

  const storyOutdated = (node) => {
    if (node.label !== "News") {
      return false;
    }
    const todayDate = new Date();
    const publishedDate = new Date(node.properties.date);
    const daysSincePublishing =
      (todayDate - publishedDate) / (1000 * 60 * 60 * 24);
    if (daysSincePublishing > dateState) {
      return true;
    }
    return false;
  };

  // Feed current node to node explorer on mouseover
  const handleMouseover = (d, refresh) => {
    if (!nodeClicked || highlightNodes.includes(d.properties._uid)) {
      setCurrentNode(d);
      setCurrentNodeColor(nodeStyles[d.label]);
      highlightNodes.push(d.properties._uid);

      if (refresh && !nodeClicked) {
        d3.selectAll(".link").style("stroke", (l) => {
          if (
            l.source.properties._uid === d.properties._uid ||
            l.target.properties._uid === d.properties._uid
          ) {
            if (l.source.properties._uid === d.properties._uid) {
              highlightNodes.push(l.target.properties._uid);
            } else {
              highlightNodes.push(l.source.properties._uid);
            }
            return "red";
          }
        });

        d3.selectAll(".node").attr("r", (n) => {
          if (highlightNodes.includes(n.properties._uid)) {
            return 40;
          } else {
            return 35;
          }
        });
      }
    }
  };

  const handleClick = (d) => {
    // Clicking on 'hidden' nodes shouldn't do anything
    if (nodeClicked && !highlightNodes.includes(d.properties._uid)) {
      return;
    }

    nodeClicked = !nodeClicked;

    d3.selectAll(".link").style("stroke", (l) => {
      if (!nodeClicked) {
        return "#999";
      }
      if (
        l.source.properties._uid === d.properties._uid ||
        l.target.properties._uid === d.properties._uid
      ) {
        return "red";
      } else {
        return "rgb(225, 225, 225)";
      }
    });

    d3.selectAll(".node")
      .style("opacity", (n) => {
        if (!highlightNodes.includes(n.properties._uid) && nodeClicked) {
          return "5%";
        } else {
          return "100%";
        }
      })
      .style("cursor", (n) => {
        if (!highlightNodes.includes(n.properties._uid) && nodeClicked) {
          return "grab";
        } else {
          return "pointer";
        }
      });

    d3.selectAll(".nodeLabel").style("display", (l) => {
      if (!highlightNodes.includes(l.properties._uid) && nodeClicked) {
        return "none";
      } else {
        return "block";
      }
    });

    d3.selectAll(".label").style("display", (d) => {
      return nodeClicked ? "none" : "block";
    });
    if (nodeClicked) {
      d3.selectAll(`.${d.properties._uid}`).style("display", "block");
    }
  };

  const handleMouseout = () => {
    console.log(nodeClicked);
    if (!nodeClicked) {
      d3.selectAll(".link").style("stroke", "#999");
      d3.selectAll(".node").attr("r", 35);
      highlightNodes = [];
    }
  };

  const handleExplorerClick = async (nodeSubstring) => {
    const node = graph.nodes.find(
      (n) =>
        n.label !== "News" &&
        n.properties.name.toUpperCase().includes(nodeSubstring.toUpperCase())
    );

    if (nodeClicked && node) {
      await handleClick(
        graph.nodes.find((n) => n.properties._uid === highlightNodes[0])
      );
      await handleMouseout();
    }
    if (node) {
      await handleMouseover(node, true);
      await handleClick(node);
      await handleMouseout();
      node.exit().remove();
      if (!nodeClicked) {
        node.select("circle").attr("r", 40);
      }
    }
  };

  useEffect(() => {
    if (!graphLoading) {
      var width = window.innerWidth;
      var height = window.innerHeight;

      const simulation = d3.layout
        .force()
        .charge(-1500)
        .linkDistance(200)
        .linkStrength(0.5)
        .size([width, height]);

      // Remove existing SVG when we rerender a new one
      simulation.nodes(graph.nodes).links(graph.links).start();
      d3.selectAll("#graph svg").remove();

      function zoomed() {
        svg.attr(
          "transform",
          "translate(" +
            d3.event.translate +
            ")" +
            " scale(" +
            d3.event.scale +
            ")"
        );
      }

      const svg = d3
        .select("#graph")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("pointer-events", "all")
        .call(d3.behavior.zoom().on("zoom", zoomed))
        .append("g");

      // Get all links and nodes to show
      const linkValues = currentLinkTypes.map((link) => link.value);
      const nodeValues = currentNodeTypes.map((node) => node.value);

      const links = graph.links.filter((link) => {
        // Don't show relationships deselected in filter
        if (!linkValues.includes(link.relationship)) {
          return false;
        }

        // Don't show relationships that don't have
        // any nodes attached to either end
        const sourceNode = isNaN(link.source)
          ? link.source
          : graph.nodes[link.source];
        const targetNode = isNaN(link.target)
          ? link.target
          : graph.nodes[link.target];
        return (
          nodeValues.includes(sourceNode.label) &&
          nodeValues.includes(targetNode.label) &&
          !storyOutdated(sourceNode) &&
          !storyOutdated(targetNode)
        );
      });

      const nodes = graph.nodes.filter((node) => {
        // Don't show nodes deselected in filter
        if (!nodeValues.includes(node.label)) {
          return false;
        }

        // Don't show nodes with no relationships
        const uniqueSourceNodesUID = Array.from(
          new Set(
            links.map((link) => {
              const id = isNaN(link.source)
                ? link.source.properties._uid
                : graph.nodes[link.source].properties._uid;
              return id;
            })
          )
        );
        const uniqueTargetNodesUID = Array.from(
          new Set(
            links.map((link) => {
              const id = isNaN(link.target)
                ? link.target.properties._uid
                : graph.nodes[link.target].properties._uid;
              return id;
            })
          )
        );
        if (
          !uniqueSourceNodesUID.includes(node.properties._uid) &&
          !uniqueTargetNodesUID.includes(node.properties._uid)
        ) {
          return false;
        }

        return true;
      });

      // Set default node for node explorer
      if (nodes[0]) {
        handleMouseover(nodes[0], false);
      }

      let link = svg.selectAll(".link").data(links);
      link
        .enter()
        .append("line")
        .attr("class", (d) => {
          var retVal = `link ${d.source.index} ${d.target.index}`;
          if (d.source.label === "News" || d.target.label === "News") {
            retVal += " story";
          }
          return retVal;
        });
      link.exit().remove();

      let node = svg.selectAll(".node").data(nodes);
      node.enter().append("g");
      node
        .append("circle")
        .attr("class", (d) => {
          return "node " + d.label;
        })
        .attr("r", 35)
        .style("fill", (d) => nodeStyles[d.label])
        .append("g");

      node
        .append("text")
        .attr("class", function (d) {
          return `nodeLabel ${d.label}`;
        })
        .attr("dx", 0)
        .attr("dy", ".35em")
        .style("font-size", "10px")
        .attr("text-anchor", "middle");

      // Wrap nodes by default
      node.call(getWrappedNodeLabel);

      node.on("mouseover", function (d) {
        handleMouseover(d, true);
        node.exit().remove();

        // Code below is to enlarge node
        if (!nodeClicked) {
          d3.select(this).select("circle").attr("r", 40);
        }
      });

      node.on("click", (d) => {
        handleClick(d);
      });

      node.on("mouseout", function (d) {
        handleMouseout();
      });

      let linkLabel = svg
        .selectAll(".linkLabel")
        .data(links)
        .enter()
        .append("text")
        .attr("fill", "black")
        .style("font", "normal 300 8px Roboto")
        .attr(
          "class",
          (d) => `label ${d.source.properties._uid} ${d.target.properties._uid}`
        )
        .attr("dy", (d) => {
          if (d.relationship === "Owners") {
            return "1em";
          } else {
            return "-0.5em";
          }
        })
        .attr("dx", (d) => {
          if (d.relationship === "Founders") {
            return "-7em";
          } else {
            return "0em";
          }
        })
        .text((d) => {
          if (
            d.relationship !== "Subsidiaries" &&
            d.relationship !== "Name" &&
            d.source.label !== "Shareholder"
          ) {
            return d.relationship;
          }
        });

      // html title attribute
      node.append("title").text((d) => d.properties.name);

      try {
        simulation.nodes(nodes).links(links).start();
      } catch (err) {
        console.log(err);
      }
      simulation.on("tick", ticked);

      function ticked() {
        link
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y);

        node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

        node.attr("transform", function (d) {
          return "translate(" + d.x + "," + d.y + ")";
        });

        linkLabel.attr("transform", (d) => {
          if (d.source.x > d.target.x) {
            const angle =
              (Math.atan2(d.source.y - d.target.y, d.source.x - d.target.x) *
                180) /
              Math.PI;
            return (
              "translate(" +
              [(d.source.x + d.target.x) / 2, (d.source.y + d.target.y) / 2] +
              ")rotate(" +
              angle +
              ")"
            );
          } else {
            const angle =
              (Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x) *
                180) /
              Math.PI;
            return (
              "translate(" +
              [(d.target.x + d.source.x) / 2, (d.target.y + d.source.y) / 2] +
              ")rotate(" +
              angle +
              ")"
            );
          }
        });
      }
    }
  }, [graphLoading]);

  return (
    <div>
      <div className="parent">
        {showHowTo && <HowTo handleClose={handleClose} />}
        <ControlPanel
          handleClick={handleExplorerClick}
          color={currentNodeColor}
          node={currentNode}
        />
        <div className={s.graph} id="graph"></div>
      </div>
    </div>
  );
}
export default Visualisation;
