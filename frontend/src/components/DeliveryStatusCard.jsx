function getStyle(status) {
  const s = status?.toLowerCase();

  if (s === "delivered") return "bg-green-100 text-green-700";
  if (s === "failed") return "bg-red-100 text-red-700";
  if (s === "sent" || s === "accepted") return "bg-blue-100 text-blue-700";

  return "bg-yellow-100 text-yellow-700";
}

export default function DeliveryStatusCard({ item }) {
  return (
    <div className={`p-2 rounded ${getStyle(item.status)}`}>
      <div className="flex justify-between">
        <span className="capitalize">{item.channel}</span>
        <span className="capitalize">{item.status}</span>
      </div>

      {item.error && (
        <p className="text-sm mt-1">{item.error}</p>
      )}
    </div>
  );
}