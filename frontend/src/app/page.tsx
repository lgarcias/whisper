"use client";
import { useState } from "react";
import { createTranscription } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function Page() {
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const router = useRouter();

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    setBusy(true);
    try {
      const { job_id } = await createTranscription(file);
      router.push(`/job/${job_id}`);
    } catch (e: any) {
      alert(e.message ?? "Upload failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="max-w-xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Whisper Website</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input type="file" accept="audio/*" onChange={e => setFile(e.target.files?.[0] ?? null)} />
        <button disabled={!file || busy} className="px-4 py-2 rounded bg-black text-white disabled:opacity-50">
          {busy ? "Uploading..." : "Transcribe"}
        </button>
      </form>
    </main>
  );
}
