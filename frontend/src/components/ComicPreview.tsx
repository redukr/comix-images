"use client";

import { Download, Share2 } from "lucide-react";
import Image from "next/image";

interface ComicPanel {
  page: number;
  title: string;
  description: string;
  speech: string;
  caption: string;
  rank: string;
  image_path?: string;
}

interface ComicPreviewProps {
  story: string;
  panels: ComicPanel[];
}

export function ComicPreview({ story, panels }: ComicPreviewProps) {
  const handleExportPDF = () => {
    // TODO: Implement PDF export
    alert("PDF export will be implemented soon!");
  };

  const handleShare = () => {
    // TODO: Implement sharing
    if (navigator.share) {
      navigator.share({
        title: "JOJ Comic",
        text: story,
        url: window.location.href,
      });
    } else {
      alert("Sharing will be implemented soon!");
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-2xl font-bold">Згенерований комікс</h3>
          <p className="text-gray-600 mt-2">{story}</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleExportPDF}
            className="flex items-center gap-2 bg-military-green text-white px-4 py-2 rounded-lg hover:bg-military-green/80"
          >
            <Download size={18} />
            PDF
          </button>
          <button
            onClick={handleShare}
            className="flex items-center gap-2 bg-joj-blue text-white px-4 py-2 rounded-lg hover:bg-joj-blue/80"
          >
            <Share2 size={18} />
            Поділитися
          </button>
        </div>
      </div>

      {/* Panels Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {panels.map((panel, index) => (
          <ComicPanelComponent key={index} panel={panel} />
        ))}
      </div>
    </div>
  );
}

function ComicPanelComponent({ panel }: { panel: ComicPanel }) {
  return (
    <div className="comic-panel p-4 space-y-4">
      {/* Panel Header */}
      <div className="flex justify-between items-start border-b-2 border-black pb-2">
        <div>
          <span className="text-xs font-bold text-military-green uppercase tracking-wide">
            Панель {panel.page}
          </span>
          <h4 className="font-bold text-lg">{panel.title}</h4>
        </div>
        <span className="text-xs bg-gray-200 px-2 py-1 rounded">
          {panel.rank}
        </span>
      </div>

      {/* Image */}
      <div className="aspect-square bg-gray-100 flex items-center justify-center relative overflow-hidden">
        {panel.image_path ? (
          <Image
            src={panel.image_path}
            alt={panel.title}
            fill
            className="object-cover"
          />
        ) : (
          <div className="text-center p-4">
            <p className="text-gray-500 text-sm">{panel.description}</p>
            <p className="text-xs text-gray-400 mt-2">
              (Зображення генерується...)
            </p>
          </div>
        )}
      </div>

      {/* Speech Bubble */}
      {panel.speech && (
        <div className="comic-speech-bubble mx-4">
          <p className="text-sm font-medium">{panel.speech}</p>
        </div>
      )}

      {/* Caption */}
      {panel.caption && (
        <p className="text-sm text-center font-serif italic text-gray-700">
          {panel.caption}
        </p>
      )}
    </div>
  );
}
