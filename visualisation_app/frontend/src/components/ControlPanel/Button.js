import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAngleLeft, faAngleRight } from "@fortawesome/free-solid-svg-icons";
import s from "./style.module.scss";

export default function Button(props) {
  return (
    <div
      className={s.buttonStyle}
      style={{ height: props.toggleFilter ? "fit-content" : "110vh" }}
      onClick={props.onClick}
    >
      <div>
        {props.toggleFilter ? (
          <FontAwesomeIcon icon={faAngleLeft} />
        ) : (
          <FontAwesomeIcon icon={faAngleRight} />
        )}
      </div>
    </div>
  );
}
