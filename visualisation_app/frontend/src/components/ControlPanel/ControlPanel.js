import React, { useState } from "react";
import NodeExplorer from "./NodeExplorer";
import Button from "./Button";
import Filter from "./Filter/Filter";
import s from "./style.module.scss";
import Toggle from "./Toggle";
import Leaderboard from "./Leaderboard/Leaderboard";

export default function ControlPanel(props) {
  const [toggleSideBar, setToggleSideBar] = useState(true);
  const [activeTab, setActiveTab] = useState("Explorer");

  const handleSideBarClick = () => {
    setToggleSideBar(!toggleSideBar);
  };

  const handleFilterClick = (e) => {
    if (activeTab !== e.target.innerHTML) {
      setActiveTab(e.target.innerHTML);
    }
  };

  return (
    <div className={s.container}>
      <Button onClick={handleSideBarClick} toggleFilter={toggleSideBar} />
      <div
        className={s.filterStyle}
        style={{ display: toggleSideBar ? "flex" : "none" }}
      >
        <Toggle toggleHook={{ activeTab, handleFilterClick }} />
        {activeTab === "Filter" && <Filter />}
        {activeTab === "Explorer" && (
          <NodeExplorer
            handleClick={props.handleClick}
            color={props.color}
            node={props.node}
          />
        )}
        {activeTab === "Trending" && <Leaderboard />}
      </div>
    </div>
  );
}
