const API_BASE_URL = "http://127.0.0.1:8000";

export async function sendOutreach(form) {
  const payload = {
    name: form.name.trim(),
    email: form.email.trim() || null,
    phone: form.phone.trim() || null,
    message: form.message.trim(),
  };

  const response = await fetch(`${API_BASE_URL}/outreach`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data?.detail || "Failed to send outreach.");
  }

  return data;
}

export function createStatusEventSource(requestId) {
  return new EventSource(`${API_BASE_URL}/outreach/${requestId}/stream`);
}