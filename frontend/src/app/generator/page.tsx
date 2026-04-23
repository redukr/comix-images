"use client";

import { useState, useEffect } from "react";
import { RankSelector } from "@/components/RankSelector";
import { ComicPreview } from "@/components/ComicPreview";
import { GenerationProgress } from "@/components/GenerationProgress";
import { generateComic, checkStatus } from "@/lib/api";
import { AlertCircle, Play } from "lucide-react";

interface Rank {
  id: string;
  name: string;
  flavor: string;
}

interface ComicPanel {
  page: number;
  title: string;
  description: string;
  speech: string;
  caption: string;
  rank: string;
  image_path?: string;
}

export default function GeneratorPage() {
  const [ranks, setRanks] = useState<Rank[]>([]);
  const [fromRank, setFromRank] = useState<string>("recruit");
  const [toRank, setToRank] = useState<string>("general");
  const [useComfy, setUseComfy] = useState<boolean>(true);
  const [useJojCards, setUseJojCards] = useState<boolean>(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [comicData, setComicData] = useState<{
    story: string;
    panels: ComicPanel[];
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Завантаження рангів при завантаженні сторінки
  useEffect(() => {
    fetch("/api/joj/ranks")
      .then((res) => res.json())
      .then((data) => {
        setRanks(data.ranks || []);
      })
      .catch((err) => {
        console.error("Failed to load ranks:", err);
        setError("Не вдалося завантажити ранги. Перевірте, чи запущено backend.");
      });
  }, []);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setProgress(0);
    setError(null);
    setComicData(null);

    try {
      // Крок 1: Запуск генерації
      setProgress(10);
      const result = await generateComic({
        rank_from: fromRank,
        rank_to: toRank,
        use_comfy: useComfy,
        use_joj_cards: useJojCards,
      });

      setProgress(30);

      // Крок 2: Якщо є job_id для генерації, чекаємо
      if (result.use_comfy && result.panels.some((p: ComicPanel) => p.generation_job_id)) {
        setProgress(50);
        
        // Чекаємо на завершення генерації зображень
        const checkInterval = setInterval(async () => {
          const status = await checkStatus(result.panels[0].generation_job_id);
          
          if (status.status === "completed") {
            clearInterval(checkInterval);
            setProgress(100);
            setComicData({
              story: result.story,
              panels: result.panels,
            });
            setIsGenerating(false);
          } else if (status.status === "error") {
            clearInterval(checkInterval);
            setError("Помилка генерації зображень");
            setIsGenerating(false);
          } else {
            setProgress((prev) => Math.min(prev + 10, 90));
          }
        }, 2000);
      } else {
        // Без генерації зображень - одразу готово
        setProgress(100);
        setComicData({
          story: result.story,
          panels: result.panels,
        });
        setIsGenerating(false);
      }
    } catch (err) {
      console.error("Generation error:", err);
      setError("Помилка генерації. Перевірте з'єднання з backend.");
      setIsGenerating(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <h2 className="text-3xl font-bold text-center">Генератор коміксів</h2>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded flex items-center gap-2">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Configuration */}
      <div className="bg-white p-6 rounded-xl shadow-md">
        <h3 className="text-xl font-bold mb-4">Налаштування</h3>
        
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <RankSelector
            label="Початковий ранг"
            ranks={ranks}
            value={fromRank}
            onChange={setFromRank}
          />
          <RankSelector
            label="Кінцевий ранг"
            ranks={ranks}
            value={toRank}
            onChange={setToRank}
          />
        </div>

        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="useComfy"
              checked={useComfy}
              onChange={(e) => setUseComfy(e.target.checked)}
              className="w-5 h-5"
            />
            <label htmlFor="useComfy" className="font-medium">
              Використовувати ComfyUI для генерації зображень
            </label>
          </div>
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="useJojCards"
              checked={useJojCards}
              onChange={(e) => setUseJojCards(e.target.checked)}
              className="w-5 h-5"
            />
            <label htmlFor="useJojCards" className="font-medium">
              Використовувати ігрові карти JOJ
            </label>
          </div>
        </div>

        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="mt-6 w-full md:w-auto bg-joj-blue text-white px-8 py-3 rounded-lg font-semibold hover:bg-joj-blue/80 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <Play size={20} />
          {isGenerating ? "Генерація..." : "Згенерувати комікс"}
        </button>
      </div>

      {/* Progress */}
      {isGenerating && (
        <GenerationProgress progress={progress} />
      )}

      {/* Preview */}
      {comicData && (
        <ComicPreview
          story={comicData.story}
          panels={comicData.panels}
        />
      )}
    </div>
  );
}
