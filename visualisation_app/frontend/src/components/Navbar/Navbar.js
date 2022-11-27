import React, { useContext } from "react";
import s from "./style.module.scss";
import { AiOutlineNodeIndex } from "react-icons/ai";
import { GraphContext } from "../../App";

function Navbar() {
  const { showHowToHook } = useContext(GraphContext);
  const { showHowTo, setShowHowTo } = showHowToHook;
  const handleClick = () => {
    setShowHowTo(true);
  };

  return (
    <div className={s.container}>
      <div className={s.navbarStyle}>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <AiOutlineNodeIndex className={s.iconStyle} />
          <h1 className={s.titleStyle}>Big Tech Visualisation</h1>
          <div
            style={{
              position: "absolute",
              right: "30px",
              color: "#1e89f3",
              padding: "7px 20px",
              border: "1px #1e89f3 solid",
              cursor: "pointer",
            }}
            onClick={handleClick}
          >
            How It Works
          </div>
        </div>
      </div>
    </div>
  );
}

export default Navbar;
