import { SPECIALTIES } from "./Specialties";
import type { Specialty } from "./Specialties";

export function CategoryDropdown({
  value,
  onChange,
}: {
  value: Specialty | "";
  onChange: (v: Specialty | "") => void;
}) {
  return (
    <select
      className="border rounded p-2"
      value={value}
      onChange={(e) => onChange(e.target.value as Specialty | "")}
    >
      <option value="">All Specialties</option>
      {SPECIALTIES.map((sp) => (
        <option key={sp} value={sp}>
          {sp}
        </option>
      ))}
    </select>
  );
}
