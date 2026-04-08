export default function OutreachForm({
  form,
  error,
  sending,
  onChange,
  onSubmit,
  onReset,
}) {
  return (
    <form onSubmit={onSubmit} className="space-y-2">
      <div>
        <label className="mb-1 block text-sm font-medium text-gray-800">
          Name <span className="text-red-500">*</span>
        </label>
        <input
          name="name"
          value={form.name}
          onChange={onChange}
          placeholder="Enter recipient name"
          className="w-full rounded-lg border border-gray-300 px-1 py-1 text-sm outline-none transition focus:border-black focus:ring-1 focus:ring-black"
        />
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-gray-800">
          Email
        </label>
        <input
          name="email"
          type="email"
          value={form.email}
          onChange={onChange}
          placeholder="name@example.com"
          className="w-full rounded-lg border border-gray-300 px-1 py-1 text-sm outline-none transition focus:border-black focus:ring-1 focus:ring-black"
        />
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-gray-800">
          Phone
        </label>
        <input
          name="phone"
          value={form.phone}
          onChange={onChange}
          placeholder="+18572756615"
          className="w-full rounded-lg border border-gray-300 px-1 py-1 text-sm outline-none transition focus:border-black focus:ring-1 focus:ring-black"
        />
        <p className="mt-1 text-xs text-gray-500">
          Use E.164 format, for example +18572756615
        </p>
      </div>

      <div>
        <label className="mb-1.5 block text-sm font-medium text-gray-800">
          Message <span className="text-red-500">*</span>
        </label>
        <textarea
          name="message"
          value={form.message}
          onChange={onChange}
          placeholder="Write your outreach message"
          rows={5}
          className="w-full rounded-lg border border-gray-300 px-3 py-3 text-sm outline-none transition focus:border-black focus:ring-1 focus:ring-black"
        />
      </div>

      {error ? (
        <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      ) : null}

      <div className="flex gap-3">
        <button
          type="submit"
          disabled={sending}
          className="flex-1 rounded-lg bg-black py-3 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {sending ? "Sending..." : "Send Outreach"}
        </button>

        <button
          type="button"
          onClick={onReset}
          className="rounded-lg border border-gray-300 px-4 py-3 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
        >
          Reset
        </button>
      </div>
    </form>
  );
}