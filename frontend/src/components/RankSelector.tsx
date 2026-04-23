"use client";

interface Rank {
  id: string;
  name: string;
  flavor: string;
}

interface RankSelectorProps {
  label: string;
  ranks: Rank[];
  value: string;
  onChange: (value: string) => void;
}

export function RankSelector({ label, ranks, value, onChange }: RankSelectorProps) {
  const selectedRank = ranks.find((r) => r.id === value);

  return (
    <div className="space-y-2">
      <label className="block font-medium text-gray-700">{label}</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-joj-blue focus:border-transparent"
      >
        {ranks.map((rank) => (
          <option key={rank.id} value={rank.id}>
            {rank.name}
          </option>
        ))}
      </select>
      {selectedRank && (
        <p className="text-sm text-gray-500 italic">{selectedRank.flavor}</p>
      )}
    </div>
  );
}
