"use client";

interface GenerationProgressProps {
  progress: number;
}

export function GenerationProgress({ progress }: GenerationProgressProps) {
  const steps = [
    { threshold: 10, label: "Ініціалізація..." },
    { threshold: 30, label: "Генерація сюжету (LLM)..." },
    { threshold: 50, label: "Підготовка зображень..." },
    { threshold: 70, label: "Генерація в ComfyUI..." },
    { threshold: 90, label: "Компонування..." },
    { threshold: 100, label: "Готово!" },
  ];

  const currentStep = steps.findLast((step) => progress >= step.threshold)?.label || "Очікування...";

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h3 className="text-lg font-bold mb-4">{currentStep}</h3>
      <div className="w-full bg-gray-200 rounded-full h-4">
        <div
          className="bg-gradient-to-r from-joj-blue to-joj-yellow h-4 rounded-full transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="text-center mt-2 text-gray-600">{progress}%</p>
    </div>
  );
}
