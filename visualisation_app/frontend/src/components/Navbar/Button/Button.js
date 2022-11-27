import React from "react";
import { IoFilterSharp } from "react-icons/io5";
import s from "./style.module.scss";

export default function Button() {
  return (
    <div className={s.buttonStyle}>
      <IoFilterSharp className={s.iconStyle} />
      <span className={s.textStyle}>Filter</span>
    </div>
  );
}
