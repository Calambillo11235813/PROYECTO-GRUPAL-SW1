import React from 'react';

// Reproductor simple para previsualizar videos
export default function VideoPlayer({ src }) {
  if (!src) return null;
  return (
    <div className="bg-slate-900 text-slate-100 p-4 rounded shadow">
      <video src={src} controls className="w-full max-h-96 rounded" />
    </div>
  );
}
