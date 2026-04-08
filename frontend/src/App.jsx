import { useState, useEffect } from "react";
import OutreachForm from "./components/OutreachForm";
import Loader from "./components/Loader";
import DeliveryStatusCard from "./components/DeliveryStatusCard";
import { sendOutreach, createStatusEventSource } from "./services/outreachApi";
import { validateOutreachForm } from "./utils/validators";

export default function App() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    message: "",
  });

  const [error, setError] = useState("");
  const [requestId, setRequestId] = useState("");
  const [results, setResults] = useState([]);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    if (!requestId) return;

    const es = createStatusEventSource(requestId);

    es.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setResults(data.results || []);
    };

    es.onerror = () => {
      es.close();
    };

    return () => es.close();
  }, [requestId]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleReset = () => {
    setForm({ name: "", email: "", phone: "", message: "" });
    setError("");
    setResults([]);
    setRequestId("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validation = validateOutreachForm(form);
    if (validation) {
      setError(validation);
      return;
    }

    setError("");
    setSending(true);

    try {
      const res = await sendOutreach(form);
      setRequestId(res.request_id);
      setResults(res.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  };

  const hasRealUpdates = results.some((r) => {
  const status = r.status?.toLowerCase();
  return status && status !== "queued";
});

const isSending = sending && !hasRealUpdates;

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 px-2 py-2">
      <div className="mx-auto w-full max-w-2xl">
        <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm md:p-4">
          <div className="mb-6">
            <p className="text-sm font-medium uppercase tracking-wide text-gray-500">
              TalentFlow Demo
            </p>
            <h1 className="mt-2 text-3xl font-semibold text-gray-900">
              Outreach Engine
            </h1>
            <p className="mt-2 text-sm text-gray-600">
              Send outreach through all available channels based on the contact
              details you provide. Email triggers email delivery, and phone
              triggers SMS and WhatsApp delivery.
            </p>
          </div>

          <OutreachForm
            form={form}
            error={error}
            sending={sending}
            onChange={handleChange}
            onSubmit={handleSubmit}
            onReset={handleReset}
          />

          {requestId && (
            <div className="mt-8 border-t border-gray-200 pt-6">
              <div className="mb-4 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">
                    Delivery Status
                  </h2>
                  <p className="text-sm text-gray-500">
                    Live updates from the backend
                  </p>
                </div>

                <div className="rounded-md bg-gray-100 px-3 py-2 text-xs text-gray-600">
                  Request ID: {requestId}
                </div>
              </div>

              <div className="space-y-2">
                {isSending && <Loader />}

                {results.map((r, i) => (
                  <DeliveryStatusCard key={i} item={r} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}