import React from "react";
import s from "./style.module.scss";

export default function Toggle(props) {
  const { activeTab, handleFilterClick } = props.toggleHook;

  return (
    <div className={s.toggleStyles}>
      <ul>
        <li
          className={activeTab !== "Explorer" ? s.inActive : undefined}
          onClick={handleFilterClick}
        >
          Explorer
        </li>
        <li
          className={activeTab !== "Filter" ? s.inActive : undefined}
          onClick={handleFilterClick}
        >
          Filter
        </li>
        <li
          className={activeTab !== "Trending" ? s.inActive : undefined}
          onClick={handleFilterClick}
        >
          Trending
        </li>
      </ul>
    </div>
  );
}
