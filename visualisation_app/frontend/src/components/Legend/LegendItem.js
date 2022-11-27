import s from "./style.module.scss";

export default function LegendItem(props) {
  return (
    <li className={s.list}>
      <div className={s.circle} style={{ backgroundColor: props.color }}></div>
      <p className={s.label}>{props.label}</p>
    </li>
  );
}
