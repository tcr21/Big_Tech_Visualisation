import LegendItem from "./LegendItem";
import s from "./style.module.scss";

export default function Legend() {
  const labels = [
    { label: "Company", color: "#0e1f58" },
    { label: "Human", color: "#eeecd0" },
    { label: "Story", color: "#d03737" },
  ];

  return (
    <div className={s.wrapper}>
      <ul>
        {labels.map((label) => (
          <LegendItem label={label.label} color={label.color} />
        ))}
      </ul>
    </div>
  );
}
