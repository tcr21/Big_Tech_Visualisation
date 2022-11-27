import React from "react";
import Select from "react-select";
import s from "./style.module.scss";
import makeAnimated from "react-select/animated";

const animatedComponents = makeAnimated();

export default function FilterElement(props) {
  return (
    <div>
      <div className={s.filterContainer}>
        <h5>{props.label}</h5>
        <div className={s.filterElement}>
          <Select
            closeMenuOnSelect={false}
            components={animatedComponents}
            isMulti
            isSearchable
            onChange={props.handleChange}
            options={props.options}
            defaultValue={props.defaultValue}
            placeholder={props.placeholder}
            styles={props.style}
          />
        </div>
      </div>
    </div>
  );
}
