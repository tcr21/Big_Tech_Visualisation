import React, { useContext, useState } from "react";
import LegendItem from "../Legend/LegendItem";
import { GraphContext } from "../../App";
import s from "./style.module.scss";
import SearchField from "react-search-field";

export default function NodeExplorer(props) {
  const { articleLinksHook, articleTitlesHook, articleSummariesHook } =
    useContext(GraphContext);
  const { articleLinks } = articleLinksHook;
  const { articleTitles } = articleTitlesHook;
  const { articleSummaries } = articleSummariesHook;
  const [value, setValue] = useState(null);

  const handleSearchClick = (i) => {
    props.handleClick(i);
    setValue("");
  };

  const handleEnter = (i, v) => {
    props.handleClick(i);
    setValue("");
  };

  const getArticlePropertyByTitle = (arr, title) => {
    let i = 0;
    articleTitles.forEach((item, j) => {
      if (item[0] === title) {
        i = j;
      }
    });
    return arr[i];
  };

  return (
    <div>
      <div>
        {props.node && props.color && (
          <div className={s.cardStyle}>
            <div className={s.labelStyle}>
              <LegendItem color={props.color} label={props.node.label} />
            </div>
            <div className={s.headerStyle}>
              <h3>{props.node.properties.name}</h3>
            </div>
            <div className={s.propertiesContainer}>
              {props.node.properties.description && (
                <div>
                  <h4>Description</h4>
                  <p>{props.node.properties.description}</p>
                </div>
              )}
              {props.node.label === "News" && (
                <div>
                  <div>
                    <h4>Article Summary</h4>
                    <p>
                      {getArticlePropertyByTitle(
                        articleSummaries,
                        props.node.properties.name
                      )}
                    </p>
                  </div>
                  <div
                    style={{
                      width: "100%",
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    <div
                      onClick={() =>
                        window.open(
                          getArticlePropertyByTitle(
                            articleLinks,
                            props.node.properties.name
                          )
                        )
                      }
                      className={s.readMore}
                    >
                      Read Article
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <div
        style={{
          marginTop: "40px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <h4 style={{ color: "white", marginBottom: "10px" }}>Search Nodes</h4>
        <SearchField
          placeholder="Enter name..."
          onChange={setValue}
          onSearchClick={handleSearchClick}
          onEnter={handleEnter}
          searchText={value}
          classNames={s.searchBar}
        />
      </div>
    </div>
  );
}
