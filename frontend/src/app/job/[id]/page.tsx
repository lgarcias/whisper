"use client";
import { useEffect, useState } from "react";
import { getStatus, getResult } from "@/lib/api";

export default function JobPage({ params }: { params: { id: string } }) {
  const id = params.id;
  const [status, setStatus] = useState("queued");
  const [text, setText] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let timer: any;
    async function tick() {
      try {
        const s = await getStatus(id);
        setStatus(s.status);
        if (s.status === "finished") {
          const r = await getResult(id);
          const payload = JSON.parse(r.json);
          setText(payload.text ?? "");
          return; // stop polling
        }
      } catch (e: any) {
        if (e.message !== "NotReady") setError(e.message ?? "Error");
      }
      timer = setTimeout(tick, 2500);
    }
    tick();
    return () => timer && clearTimeout(timer);
  }, [id]);

  return (
    <main className="max-w-3xl mx-auto p-6">
      <h1 className="text-xl font-semibold mb-2">Job {id}</h1>
      <p className="mb-4">Status: <span className="font-mono">{status}</span></p>
      {error && <p className="text-red-600">{error}</p>}
      {text && (
        <>
          <h2 className="text-lg font-semibold mb-2">Transcript</h2>
          <pre className="whitespace-pre-wrap p-4 rounded border">{text}</pre>
        </>
      )}
    </main>
  );
}
