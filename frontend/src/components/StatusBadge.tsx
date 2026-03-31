type Props = {
  value: string;
};

export default function StatusBadge({ value }: Props) {
  return (
    <span
      style={{
        display: "inline-block",
        padding: "4px 10px",
        border: "1px solid #cbd5e1",
        borderRadius: 999,
        fontSize: 12,
        fontWeight: 600,
        textTransform: "uppercase",
        letterSpacing: 0.4,
        backgroundColor: "#f8fafc",
      }}
    >
      {value.replaceAll("_", " ")}
    </span>
  );
}